"""
Blu Visual Teacher - Backend REST API Server.
Coordinates Stage 1 (Concept input), Stage 2 (Lesson planner),
Stage 3 & 4 (Multilingual narration & audio sync), and Stage 5 (720p MP4 export).
"""

import os
import sys
import time
import json
import logging
import platform
import psutil
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add backend directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from schema import validate_lesson_plan
from planner import plan_lesson
from tts_engine import process_lesson_audio, synthesize_scene_audio, VOICE_MAPPING
from video_renderer import export_lesson_mp4
from lesson_cache import get_cached_lesson, save_cached_lesson

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
)
logger = logging.getLogger("blu_teacher.server")

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)
CORS(app)

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
GENERATED_DIR = os.path.join(BASE_DIR, "static", "generated")
PREGENERATED_DIR = os.path.join(BASE_DIR, "pregenerated")
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(PREGENERATED_DIR, exist_ok=True)


@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_frontend_assets(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/pregenerated/<path:filename>")
def serve_pregenerated(filename):
    return send_from_directory(PREGENERATED_DIR, filename)


@app.route("/api/status", methods=["GET"])
def get_system_status():
    """
    Returns system telemetry, CPU/RAM footprint, offline readiness,
    and available languages & voices.
    """
    mem = psutil.virtual_memory()
    return jsonify({
        "status": "online_or_offline_ready",
        "system": {
            "os": platform.system(),
            "cpu": platform.processor(),
            "ram_total_gb": round(mem.total / (1024 ** 3), 2),
            "ram_available_gb": round(mem.available / (1024 ** 3), 2),
            "python_version": platform.python_version()
        },
        "supported_languages": [
            {"code": "en", "name": "English (Indian Accent)", "script": "Latin"},
            {"code": "hi", "name": "Hindi (हिंदी)", "script": "Devanagari"},
            {"code": "ta", "name": "Tamil (தமிழ்)", "script": "Tamil"},
            {"code": "te", "name": "Telugu (తెలుగు)", "script": "Telugu"},
            {"code": "mr", "name": "Marathi (मराठी)", "script": "Devanagari"},
            {"code": "bn", "name": "Bengali (বাংলা)", "script": "Bengali"}
        ],
        "voices": VOICE_MAPPING,
        "features": {
            "offline_planner": True,
            "ollama_connectable": True,
            "voice_length_sync": True,
            "export_720p_mp4": True,
            "srt_captions": True,
            "scene_editor": True
        }
    })


@app.route("/api/plan", methods=["POST"])
def api_plan_lesson():
    """
    Stage 1 & 2: Receives topic, level, language.
    Plans lesson via local LLM or verified fallback, checks schema, returns JSON.
    Tracks speed metrics.
    """
    data = request.json or {}
    topic = data.get("topic", "How a Python loop works")
    level = data.get("level", "beginner")
    language = data.get("language", "en")
    target_length = data.get("target_length", 45)
    use_cache = data.get("use_cache", True)

    t0 = time.time()

    # Check cache first if requested
    if use_cache:
        cached = get_cached_lesson(topic, language, level)
        if cached:
            cached["metrics"] = {
                "planning_time_sec": 0.01,
                "cached": True
            }
            return jsonify(cached)

    # Run Planner
    lesson_plan = plan_lesson(
        topic=topic,
        level=level,
        language=language
    )
    lesson_plan["target_length"] = target_length

    planning_time = round(time.time() - t0, 3)

    # Validate output schema
    is_valid, error = validate_lesson_plan(lesson_plan)
    if not is_valid:
        logger.error(f"Schema validation failed: {error}")
        return jsonify({"error": f"Schema validation failed: {error}"}), 400

    lesson_plan["metrics"] = {
        "planning_time_sec": planning_time,
        "cached": False
    }

    return jsonify(lesson_plan)


@app.route("/api/audio", methods=["POST"])
def api_process_audio():
    """
    Stage 4: Generates multilingual narration audio for each scene.
    Enforces key rule: voice duration drives scene length!
    """
    data = request.json or {}
    lesson_plan = data.get("lesson_plan")
    gender = data.get("gender", "female")
    speed = float(data.get("speed", 1.0))

    if not lesson_plan or "scenes" not in lesson_plan:
        return jsonify({"error": "Missing lesson_plan with scenes"}), 400

    t0 = time.time()
    updated_plan = process_lesson_audio(
        lesson_plan=lesson_plan,
        gender=gender,
        speed=speed
    )
    audio_time = round(time.time() - t0, 3)

    if "metrics" not in updated_plan:
        updated_plan["metrics"] = {}
    updated_plan["metrics"]["audio_generation_time_sec"] = audio_time

    # Save to lesson cache
    topic = updated_plan.get("title", "lesson")
    lang = updated_plan.get("language", "en")
    level = updated_plan.get("level", "beginner")
    save_cached_lesson(topic, lang, level, updated_plan)

    return jsonify(updated_plan)


@app.route("/api/regenerate_scene", methods=["POST"])
def api_regenerate_scene():
    """
    Bonus: Edit before render.
    Re-synthesizes audio for an edited scene without affecting the rest of the lesson.
    """
    data = request.json or {}
    scene = data.get("scene")
    language = data.get("language", "en")
    gender = data.get("gender", "female")
    speed = float(data.get("speed", 1.0))

    if not scene or "narration" not in scene:
        return jsonify({"error": "Missing scene or narration"}), 400

    audio_url, audio_dur = synthesize_scene_audio(
        text=scene["narration"],
        language=language,
        gender=gender,
        speed=speed,
        force_refresh=True
    )

    scene["audio_url"] = audio_url
    scene["audio_path"] = os.path.join(BASE_DIR, "static", "cache", "audio", os.path.basename(audio_url))
    scene["audio_duration"] = audio_dur
    scene["duration"] = round(audio_dur + 0.8, 2)

    return jsonify(scene)


@app.route("/api/revoice", methods=["POST"])
def api_revoice():
    """
    Bonus: Switch that re-voices a finished lesson into another language
    without re-planning it from scratch.
    """
    data = request.json or {}
    lesson_plan = data.get("lesson_plan")
    new_language = data.get("new_language", "hi")
    gender = data.get("gender", "female")
    speed = float(data.get("speed", 1.0))

    if not lesson_plan:
        return jsonify({"error": "Missing lesson_plan"}), 400

    # Obtain matching translated lesson or translate narrations
    topic = lesson_plan.get("title", "")
    revoiced_plan = plan_lesson(topic=topic, level=lesson_plan.get("level", "beginner"), language=new_language)
    
    # Process audio for new language
    processed = process_lesson_audio(revoiced_plan, gender=gender, speed=speed)
    return jsonify(processed)


@app.route("/api/export", methods=["POST"])
def api_export_mp4():
    """
    Stage 5: Renders 1280x720 video frames with animated scenes,
    combines with voice-over audio and captions, and exports downloadable MP4 & SRT.
    """
    data = request.json or {}
    lesson_plan = data.get("lesson_plan")
    if not lesson_plan or "scenes" not in lesson_plan:
        return jsonify({"error": "Missing lesson_plan"}), 400

    # Ensure audio paths are present
    if not lesson_plan.get("scenes", [{}])[0].get("audio_path"):
        lesson_plan = process_lesson_audio(lesson_plan)

    t0 = time.time()
    title_slug = "".join(c if c.isalnum() else "_" for c in lesson_plan.get("title", "lesson"))[:20]
    lang = lesson_plan.get("language", "en")
    ts = int(time.time())
    output_filename = f"{title_slug}_{lang}_{ts}.mp4"
    output_filepath = os.path.join(GENERATED_DIR, output_filename)

    success = export_lesson_mp4(lesson_plan, output_filepath)
    render_time = round(time.time() - t0, 3)

    if not success:
        return jsonify({"error": "MP4 rendering failed"}), 500

    srt_filename = output_filename.replace(".mp4", ".srt")

    return jsonify({
        "success": True,
        "video_url": f"/static/generated/{output_filename}",
        "srt_url": f"/static/generated/{srt_filename}",
        "render_time_sec": render_time,
        "resolution": "1280x720 (720p)",
        "codec": "H.264 / AAC",
        "total_duration": lesson_plan.get("total_duration", 0)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Blu Visual Teacher server on port {port}...")
    app.run(host="127.0.0.1", port=port, debug=False)
