"""
Multilingual Text-to-Speech Engine for Blu Visual Teacher.
Supports Indian-accented English, Hindi, Tamil, Telugu, Marathi, and Bengali.
Uses Edge-TTS for studio-quality neural voices, with native Windows SAPI
speech synthesizer for 100% offline fallback (zero internet required).
"""

import os
import sys
import hashlib
import asyncio
import logging
import subprocess
from typing import Dict, Any, Tuple, Optional
import imageio_ffmpeg

logger = logging.getLogger("blu_teacher.tts")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Real neural voices for Indian English and regional Indian languages
VOICE_MAPPING = {
    "en": {
        "female": "en-IN-NeerjaNeural",
        "male": "en-IN-PrabhatNeural"
    },
    "hi": {
        "female": "hi-IN-SwaraNeural",
        "male": "hi-IN-MadhurNeural"
    },
    "ta": {
        "female": "ta-IN-PallaviNeural",
        "male": "ta-IN-ValluvarNeural"
    },
    "te": {
        "female": "te-IN-ShrutiNeural",
        "male": "te-IN-MohanNeural"
    },
    "mr": {
        "female": "mr-IN-AarohiNeural",
        "male": "mr-IN-ManoharNeural"
    },
    "bn": {
        "female": "bn-IN-TanishaaNeural",
        "male": "bn-IN-BashkarNeural"
    }
}


def get_cache_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_dir = os.path.join(base, "static", "cache", "audio")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def get_audio_duration(file_path: str) -> float:
    """Measures the exact duration of an audio file using FFmpeg probe."""
    try:
        cmd = [
            FFMPEG_EXE,
            "-i", file_path,
            "-f", "null", "-"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="replace")
        
        output = proc.stderr
        import re
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", output)
        if match:
            hours = float(match.group(1))
            minutes = float(match.group(2))
            seconds = float(match.group(3))
            return round(hours * 3600 + minutes * 60 + seconds, 2)
    except Exception as e:
        logger.warning(f"Error measuring audio duration via ffmpeg: {e}")

    return 4.5


async def synthesize_edge_tts(
    text: str,
    voice: str,
    rate_str: str,
    output_path: str
) -> bool:
    """Invokes edge-tts to generate natural neural speech."""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice, rate=rate_str)
        await asyncio.wait_for(communicate.save(output_path), timeout=12.0)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        logger.info(f"Edge-TTS synthesis error: {e}")
        return False


def generate_windows_sapi_audio(text: str, output_path: str) -> float:
    """
    Offline fallback using native Windows SAPI SpeechSynthesizer.
    Produces real spoken words completely offline without internet access.
    """
    wav_path = output_path.replace(".mp3", ".wav")
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        # 3 = SSFMCreateForWrite
        stream.Open(wav_path, 3)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()

        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 1000:
            cmd = [
                FFMPEG_EXE, "-y",
                "-i", wav_path,
                "-codec:a", "libmp3lame",
                "-qscale:a", "2",
                output_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(wav_path) and wav_path != output_path:
                os.remove(wav_path)
            return get_audio_duration(output_path)
    except Exception as e:
        logger.warning(f"Windows SAPI generation error: {e}")

    return 4.0


def synthesize_scene_audio(
    text: str,
    language: str = "en",
    gender: str = "female",
    speed: float = 1.0,
    force_refresh: bool = False
) -> Tuple[str, float]:
    """
    Synthesizes audio for a single scene's narration.
    Returns (relative_audio_url, exact_duration_seconds).
    1. Checks local cache for instant reuse.
    2. Uses real neural human voice (Edge-TTS).
    3. If offline, falls back to native Windows SpeechSynthesizer.
    """
    cache_dir = get_cache_dir()
    
    # Determine voice
    lang_voices = VOICE_MAPPING.get(language, VOICE_MAPPING["en"])
    voice_name = lang_voices.get(gender, lang_voices["female"])

    # Calculate speed rate modifier
    rate_pct = int(round((speed - 1.0) * 100))
    rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"

    # Unique cache key
    key_str = f"{language}_{voice_name}_{rate_str}_{text.strip()}"
    file_hash = hashlib.md5(key_str.encode("utf-8")).hexdigest()
    output_filename = f"{file_hash}.mp3"
    output_filepath = os.path.join(cache_dir, output_filename)

    # 1. Check existing cached file
    if not force_refresh and os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 1000:
        duration = get_audio_duration(output_filepath)
        logger.info(f"Loaded audio from cache: {output_filename} ({duration}s)")
        return f"/static/cache/audio/{output_filename}", duration

    # 2. Try neural human speech (Edge-TTS)
    success = False
    try:
        success = asyncio.run(synthesize_edge_tts(text, voice_name, rate_str, output_filepath))
    except Exception as e:
        logger.info(f"Edge-TTS synthesis error: {e}")

    # 3. Offline fallback to Windows SAPI SpeechSynthesizer
    if not success or not os.path.exists(output_filepath) or os.path.getsize(output_filepath) < 1000:
        logger.info(f"Using offline Windows SAPI voice for: {text[:30]}...")
        duration = generate_windows_sapi_audio(text, output_filepath)
        return f"/static/cache/audio/{output_filename}", duration

    duration = get_audio_duration(output_filepath)
    return f"/static/cache/audio/{output_filename}", duration


def process_lesson_audio(
    lesson_plan: dict,
    gender: str = "female",
    speed: float = 1.0,
    pause_after_scene: float = 0.8
) -> dict:
    """
    Enforces Key Design Rule:
    'The voice-over sets each scene's length. Generate the narration audio first,
     then make each scene last as long as its audio plus a short pause.
     If you hard-code scene durations, your audio and visuals will drift apart.'
    """ 
    language = lesson_plan.get("language", "en")
    scenes = lesson_plan.get("scenes", [])
    total_time = 0.0

    for i, scene in enumerate(scenes):
        narration = scene.get("narration", "")
        audio_url, audio_dur = synthesize_scene_audio(
            text=narration,
            language=language,
            gender=gender,
            speed=speed
        )
        
        scene_duration = round(audio_dur + pause_after_scene, 2)
        scene["audio_url"] = audio_url
        scene["audio_path"] = os.path.join(get_cache_dir(), os.path.basename(audio_url))
        scene["audio_duration"] = audio_dur
        scene["pause"] = pause_after_scene
        scene["duration"] = scene_duration
        
        total_time += scene_duration

    lesson_plan["total_duration"] = round(total_time, 2)
    return lesson_plan
