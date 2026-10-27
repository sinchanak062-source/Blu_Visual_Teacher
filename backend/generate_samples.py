"""
Script to pre-generate benchmark 720p MP4 lessons for judges.
Creates:
1. python_loop_en.mp4 (English)
2. python_loop_hi.mp4 (Hindi)
3. binary_search_en.mp4 (English)
4. binary_search_hi.mp4 (Hindi)
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from planner import plan_lesson
from tts_engine import process_lesson_audio
from video_renderer import export_lesson_mp4

PREGEN_DIR = os.path.join(BASE_DIR, "pregenerated")
os.makedirs(PREGEN_DIR, exist_ok=True)

TARGETS = [
    ("Python Loops", "beginner", "en", "python_loop_en.mp4"),
    ("Python Loops", "beginner", "hi", "python_loop_hi.mp4"),
    ("Binary Search", "intermediate", "en", "binary_search_en.mp4"),
    ("Binary Search", "intermediate", "hi", "binary_search_hi.mp4")
]

def main():
    print("=== Blu Visual Teacher: Pre-generating MP4 Lessons ===", flush=True)
    for topic, level, lang, filename in TARGETS:
        out_path = os.path.join(PREGEN_DIR, filename)
        print(f"\n[+] Generating {filename} ({topic} in {lang})...", flush=True)
        t0 = time.time()
        
        # 1. Plan
        plan = plan_lesson(topic=topic, level=level, language=lang)
        print(f"    - Planned: {plan['title']} ({len(plan['scenes'])} scenes)", flush=True)
        
        # 2. Audio & duration sync
        plan = process_lesson_audio(plan, gender="female", speed=1.0)
        print(f"    - Audio synced: Total duration {plan['total_duration']}s", flush=True)
        
        # 3. 720p Video Export
        success = export_lesson_mp4(plan, out_path)
        dur = round(time.time() - t0, 2)
        if success and os.path.exists(out_path):
            size_mb = round(os.path.getsize(out_path) / (1024 * 1024), 2)
            print(f"    [✓] SUCCESS: {filename} generated in {dur}s ({size_mb} MB, 720p)", flush=True)
        else:
            print(f"    [X] FAILED for {filename}", flush=True)

if __name__ == "__main__":
    main()
