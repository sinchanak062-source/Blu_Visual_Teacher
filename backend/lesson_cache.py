"""
Lesson Cache Management for Blu Visual Teacher.
Caches generated lesson plans and exported videos by topic, language, and version
so repeat requests are served instantly without redundant re-generation.
"""

import os
import json
import hashlib
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("blu_teacher.cache")


def get_cache_root() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = os.path.join(base, "static", "cache", "lessons")
    os.makedirs(root, exist_ok=True)
    return root


def make_cache_key(topic: str, language: str, level: str, version: int = 1) -> str:
    norm_topic = topic.strip().lower()
    raw = f"{norm_topic}_{language}_{level}_v{version}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def get_cached_lesson(topic: str, language: str, level: str = "beginner", version: int = 1) -> Optional[dict]:
    """Retrieves a previously generated lesson from cache if available."""
    key = make_cache_key(topic, language, level, version)
    file_path = os.path.join(get_cache_root(), f"{key}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Cache hit for '{topic}' ({language})")
                return data
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")
    return None


def save_cached_lesson(topic: str, language: str, level: str, lesson_plan: dict, version: int = 1):
    """Saves a generated lesson plan into disk cache."""
    key = make_cache_key(topic, language, level, version)
    file_path = os.path.join(get_cache_root(), f"{key}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(lesson_plan, f, indent=2, ensure_ascii=False)
        logger.info(f"Cached lesson for '{topic}' ({language}) -> {key}.json")
    except Exception as e:
        logger.error(f"Error saving to cache: {e}")
