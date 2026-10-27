"""
Schema definitions and validation for Blu Visual Teacher lesson plans.
"""

from typing import List, Optional, Union, Dict, Any
from jsonschema import validate, ValidationError

LESSON_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 3},
        "level": {"type": "string", "enum": ["beginner", "intermediate", "advanced"]},
        "language": {"type": "string", "enum": ["en", "hi", "ta", "te", "mr", "bn", "kn"]},
        "target_length": {"type": "integer", "minimum": 20, "maximum": 180},
        "scenes": {
            "type": "array",
            "minItems": 3,
            "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["title_card", "code_walkthrough", "diagram", "timeline", "quiz"]
                    },
                    "heading": {"type": "string", "minLength": 2},
                    "narration": {"type": "string", "minLength": 5},
                    # Scene specific fields:
                    "code": {"type": "string"},
                    "highlight_lines": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "items": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "arrows": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "steps": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "correct_index": {"type": "integer"},
                    "duration": {"type": "number"}
                },
                "required": ["type", "heading", "narration"]
            }
        }
    },
    "required": ["title", "level", "language", "scenes"]
}


def validate_lesson_plan(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validates a lesson plan dict against the strict LESSON_SCHEMA.
    Returns (True, None) if valid, or (False, error_message).
    """
    try:
        validate(instance=data, schema=LESSON_SCHEMA)
        
        # Additional semantic checks
        for i, scene in enumerate(data.get("scenes", [])):
            stype = scene.get("type")
            if stype == "code_walkthrough" and not scene.get("code"):
                return False, f"Scene {i+1} is code_walkthrough but missing 'code' field"
            if stype == "diagram" and not scene.get("items"):
                return False, f"Scene {i+1} is diagram but missing 'items' field"
            if stype == "timeline" and not scene.get("steps"):
                return False, f"Scene {i+1} is timeline but missing 'steps' field"
            if stype == "quiz":
                if not scene.get("question") or not scene.get("options"):
                    return False, f"Scene {i+1} is quiz but missing 'question' or 'options'"
                if "correct_index" not in scene:
                    scene["correct_index"] = 0
                    
        return True, None
    except ValidationError as e:
        return False, e.message
    except Exception as e:
        return False, str(e)
