"""
720p Video Renderer & FFmpeg MP4 Exporter for Blu Visual Teacher.
Generates 1280x720 H.264 video with AAC audio, burned-in multilingual captions,
progress bar, step headings, and dynamic animated scene components.
"""

import os
import sys
import subprocess
import logging
from typing import Dict, Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

logger = logging.getLogger("blu_teacher.video")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

WIDTH = 1280
HEIGHT = 720
FPS = 24

# Color Palette (Dark modern educational theme)
BG_TOP = (13, 17, 23)        # #0D1117
BG_BOTTOM = (22, 27, 34)     # #161B22
ACCENT_BLUE = (56, 139, 253) # #388BFD
ACCENT_CYAN = (88, 166, 255) # #58A6FF
ACCENT_GREEN = (63, 185, 80) # #3FB950
ACCENT_PURPLE = (187, 128, 247) # #BB80F7
ACCENT_ORANGE = (240, 136, 62)  # #F0883E
TEXT_WHITE = (240, 246, 252) # #F0F6FC
TEXT_MUTED = (139, 148, 158) # #8B949E
CARD_BG = (22, 27, 34)
CARD_BORDER = (48, 54, 61)
CAPTION_BG = (17, 21, 28, 235)


def get_fonts():
    """Loads system fonts for Indian scripts and monospace code."""
    nirmala_path = "C:/Windows/Fonts/Nirmala.ttc"
    segoe_path = "C:/Windows/Fonts/segoeui.ttf"
    code_path = "C:/Windows/Fonts/consola.ttf"

    font_family = nirmala_path if os.path.exists(nirmala_path) else segoe_path

    try:
        title_font = ImageFont.truetype(font_family, 36)
        heading_font = ImageFont.truetype(font_family, 30)
        sub_font = ImageFont.truetype(font_family, 22)
        caption_font = ImageFont.truetype(font_family, 23)
        code_font = ImageFont.truetype(code_path if os.path.exists(code_path) else font_family, 24)
        small_font = ImageFont.truetype(font_family, 16)
    except Exception:
        title_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        caption_font = ImageFont.load_default()
        code_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    return {
        "title": title_font,
        "heading": heading_font,
        "sub": sub_font,
        "caption": caption_font,
        "code": code_font,
        "small": small_font
    }


def draw_background(draw: ImageDraw.ImageDraw):
    """Draws a vertical dark gradient with faint ambient grid lines."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Ambient grid lines (subtle dark tech aesthetic)
    grid_color = (255, 255, 255, 12)
    for x in range(0, WIDTH, 80):
        draw.line([(x, 0), (x, HEIGHT)], fill=(20, 26, 36))
    for y in range(0, HEIGHT, 80):
        draw.line([(0, y), (WIDTH, y)], fill=(20, 26, 36))


def render_top_bar(
    draw: ImageDraw.ImageDraw,
    lesson_title: str,
    scene_idx: int,
    total_scenes: int,
    overall_progress: float,
    fonts: dict
):
    """Renders top header badge, lesson title, scene counter, and smooth progress bar."""
    # Top badge
    draw.rounded_rectangle([40, 20, 200, 52], radius=6, fill=(33, 38, 45), outline=(56, 139, 253))
    draw.text((54, 26), "BLU TEACHER", fill=ACCENT_CYAN, font=fonts["small"])

    # Lesson title (truncated if long)
    title_display = lesson_title if len(lesson_title) < 45 else lesson_title[:42] + "..."
    draw.text((220, 24), title_display, fill=TEXT_WHITE, font=fonts["sub"])

    # Scene counter
    counter_str = f"Scene {scene_idx + 1} of {total_scenes}"
    draw.rounded_rectangle([WIDTH - 180, 20, WIDTH - 40, 52], radius=6, fill=(33, 38, 45))
    draw.text((WIDTH - 165, 26), counter_str, fill=TEXT_MUTED, font=fonts["small"])

    # Smooth progress bar (y: 64 to 70)
    bar_x1 = 40
    bar_x2 = WIDTH - 40
    draw.rounded_rectangle([bar_x1, 64, bar_x2, 70], radius=3, fill=(33, 38, 45))
    
    fill_width = int(bar_x1 + (bar_x2 - bar_x1) * max(0.01, min(1.0, overall_progress)))
    draw.rounded_rectangle([bar_x1, 64, fill_width, 70], radius=3, fill=ACCENT_BLUE)


def render_scene_heading(
    draw: ImageDraw.ImageDraw,
    heading: str,
    scene_idx: int,
    fonts: dict
):
    """Renders Step badge and main scene title."""
    badge_text = f"STEP {scene_idx + 1}"
    draw.rounded_rectangle([50, 92, 140, 122], radius=4, fill=(56, 139, 253, 50), outline=ACCENT_BLUE)
    draw.text((62, 97), badge_text, fill=ACCENT_CYAN, font=fonts["small"])
    draw.text((155, 90), heading, fill=TEXT_WHITE, font=fonts["heading"])


def render_title_card(
    draw: ImageDraw.ImageDraw,
    scene: dict,
    level: str,
    language: str,
    t_scene: float,
    fonts: dict
):
    """Renders animated Title Card scene."""
    # Main hero card
    cx1, cy1, cx2, cy2 = 180, 160, WIDTH - 180, 560
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=16, fill=(18, 23, 32), outline=(56, 139, 253))

    # Inner decorative glow circle
    pulse = int(12 * (0.5 + 0.5 * (t_scene % 1.5) / 1.5))
    draw.ellipse([WIDTH // 2 - 60 - pulse, 220 - pulse, WIDTH // 2 + 60 + pulse, 340 + pulse], outline=(88, 166, 255, 80), width=2)
    draw.ellipse([WIDTH // 2 - 50, 230, WIDTH // 2 + 50, 330], fill=(30, 41, 59), outline=ACCENT_BLUE, width=3)
    
    # Hero icon symbol: graduation cap / play symbol
    draw.polygon([
        (WIDTH // 2 - 15, 260),
        (WIDTH // 2 + 25, 280),
        (WIDTH // 2 - 15, 300)
    ], fill=ACCENT_CYAN)

    # Heading
    head = scene.get("heading", "")
    draw.text((WIDTH // 2, 380), head, fill=TEXT_WHITE, font=fonts["title"], anchor="mm")

    # Badges row: Level, Offline Ready, Audio synced
    badge_w = 140
    bx = WIDTH // 2 - 160
    draw.rounded_rectangle([bx, 440, bx + badge_w, 474], radius=6, fill=(33, 38, 45), outline=ACCENT_GREEN)
    draw.text((bx + 20, 448), f"Level: {level.capitalize()}", fill=ACCENT_GREEN, font=fonts["small"])

    bx2 = WIDTH // 2 + 20
    draw.rounded_rectangle([bx2, 440, bx2 + badge_w, 474], radius=6, fill=(33, 38, 45), outline=ACCENT_PURPLE)
    draw.text((bx2 + 22, 448), f"Lang: {language.upper()}", fill=ACCENT_PURPLE, font=fonts["small"])


def render_code_walkthrough(
    draw: ImageDraw.ImageDraw,
    scene: dict,
    t_scene: float,
    fonts: dict
):
    """Renders macOS/VSCode-like Code walkthrough IDE window with glowing line highlight."""
    wx1, wy1, wx2, wy2 = 140, 155, WIDTH - 140, 570
    draw.rounded_rectangle([wx1, wy1, wx2, wy2], radius=12, fill=(18, 22, 28), outline=(48, 54, 61))

    # Top title bar of window
    draw.rounded_rectangle([wx1, wy1, wx2, wy1 + 42], radius=12, fill=(28, 33, 40))
    draw.rectangle([wx1, wy1 + 25, wx2, wy1 + 42], fill=(28, 33, 40))

    # Window traffic light dots
    draw.ellipse([wx1 + 16, wy1 + 14, wx1 + 28, wy1 + 26], fill=(255, 95, 87)) # red
    draw.ellipse([wx1 + 36, wy1 + 14, wx1 + 48, wy1 + 26], fill=(254, 188, 46)) # yellow
    draw.ellipse([wx1 + 56, wy1 + 14, wx1 + 68, wy1 + 26], fill=(40, 200, 64))  # green

    # File tab
    draw.rounded_rectangle([wx1 + 90, wy1 + 8, wx1 + 260, wy1 + 38], radius=6, fill=(18, 22, 28))
    draw.text((wx1 + 115, wy1 + 14), "lesson_code.py", fill=TEXT_MUTED, font=fonts["small"])

    # Code lines
    code_text = scene.get("code", "")
    lines = code_text.split("\n")
    highlight_lines = scene.get("highlight_lines", [1])

    line_y = wy1 + 60
    for i, line in enumerate(lines):
        line_num = i + 1
        is_highlighted = line_num in highlight_lines

        if is_highlighted:
            # Glowing highlighted line background
            draw.rectangle([wx1 + 2, line_y - 4, wx2 - 2, line_y + 32], fill=(31, 61, 92))
            draw.rectangle([wx1 + 2, line_y - 4, wx1 + 8, line_y + 32], fill=ACCENT_CYAN)
            # Animated focus arrow
            arrow_shift = int(4 * (t_scene % 1.0))
            draw.text((wx1 + 15 + arrow_shift, line_y), "➔", fill=ACCENT_CYAN, font=fonts["code"])

        # Line number
        draw.text((wx1 + 45, line_y), f"{line_num:2d}", fill=TEXT_MUTED if not is_highlighted else ACCENT_CYAN, font=fonts["code"])
        
        # Line text
        text_color = TEXT_WHITE if not is_highlighted else (255, 255, 255)
        draw.text((wx1 + 90, line_y), line, fill=text_color, font=fonts["code"])

        line_y += 38


def render_diagram(
    draw: ImageDraw.ImageDraw,
    scene: dict,
    t_scene: float,
    fonts: dict
):
    """Renders animated connected node diagram with directional arrows and state badges."""
    items = scene.get("items", ["Step 1", "Step 2", "Step 3"])
    n = len(items)
    if n == 0:
        return

    cy = 340
    spacing = (WIDTH - 240) // n
    box_w = min(220, spacing - 40)
    box_h = 130

    active_idx = int((t_scene / max(0.1, scene.get("duration", 5.0))) * n)
    active_idx = min(n - 1, max(0, active_idx))

    positions = []
    for i, item in enumerate(items):
        cx = 120 + i * spacing + spacing // 2
        bx1 = cx - box_w // 2
        by1 = cy - box_h // 2
        bx2 = cx + box_w // 2
        by2 = cy + box_h // 2
        positions.append((cx, cy, bx1, by1, bx2, by2))

    # Draw connecting arrows between boxes
    for i in range(n - 1):
        x_start = positions[i][4] + 6
        x_end = positions[i + 1][2] - 6
        arrow_y = cy
        is_arrow_active = i < active_idx
        arrow_color = ACCENT_CYAN if is_arrow_active else CARD_BORDER
        
        draw.line([(x_start, arrow_y), (x_end, arrow_y)], fill=arrow_color, width=4)
        # Arrowhead
        draw.polygon([
            (x_end, arrow_y),
            (x_end - 12, arrow_y - 8),
            (x_end - 12, arrow_y + 8)
        ], fill=arrow_color)

    # Draw node boxes
    for i, item in enumerate(items):
        cx, cy_box, bx1, by1, bx2, by2 = positions[i]
        is_active = (i == active_idx)
        
        box_bg = (28, 48, 75) if is_active else CARD_BG
        box_border = ACCENT_CYAN if is_active else CARD_BORDER
        
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=14, fill=box_bg, outline=box_border, width=3 if is_active else 1)
        
        # Step number badge
        draw.rounded_rectangle([bx1 + 12, by1 + 12, bx1 + 60, by1 + 36], radius=4, fill=(56, 139, 253, 60))
        draw.text((bx1 + 20, by1 + 14), f"#{i+1}", fill=ACCENT_CYAN, font=fonts["small"])

        # Item text
        draw.text((cx, cy_box + 10), item, fill=TEXT_WHITE, font=fonts["sub"], anchor="mm")


def render_timeline(
    draw: ImageDraw.ImageDraw,
    scene: dict,
    t_scene: float,
    fonts: dict
):
    """Renders milestone lifecycle timeline."""
    steps = scene.get("steps", ["Start", "Process", "Complete"])
    n = len(steps)
    if n == 0:
        return

    track_y = 330
    x_start = 160
    x_end = WIDTH - 160
    spacing = (x_end - x_start) / max(1, n - 1)

    # Base track line
    draw.line([(x_start, track_y), (x_end, track_y)], fill=(48, 54, 61), width=6)

    # Progress fill
    progress = min(1.0, t_scene / max(1.0, scene.get("duration", 5.0)))
    fill_x = x_start + (x_end - x_start) * progress
    draw.line([(x_start, track_y), (fill_x, track_y)], fill=ACCENT_BLUE, width=6)

    # Step milestone circles
    for i, step in enumerate(steps):
        cx = int(x_start + i * spacing)
        step_passed = fill_x >= cx - 5
        
        c_fill = ACCENT_CYAN if step_passed else (33, 38, 45)
        c_outline = (255, 255, 255) if step_passed else CARD_BORDER
        
        draw.ellipse([cx - 22, track_y - 22, cx + 22, track_y + 22], fill=c_fill, outline=c_outline, width=3)
        draw.text((cx, track_y), str(i + 1), fill=(0, 0, 0) if step_passed else TEXT_MUTED, font=fonts["small"], anchor="mm")

        # Step label text below
        draw.text((cx, track_y + 40), step, fill=TEXT_WHITE if step_passed else TEXT_MUTED, font=fonts["sub"], anchor="mt")


def render_quiz(
    draw: ImageDraw.ImageDraw,
    scene: dict,
    t_scene: float,
    fonts: dict
):
    """Renders interactive quiz card with answer revelation animation."""
    qx1, qy1, qx2, qy2 = 140, 160, WIDTH - 140, 560
    draw.rounded_rectangle([qx1, qy1, qx2, qy2], radius=14, fill=CARD_BG, outline=CARD_BORDER)

    # Question Header
    draw.rounded_rectangle([qx1 + 24, qy1 + 18, qx1 + 180, qy1 + 48], radius=6, fill=(187, 128, 247, 40), outline=ACCENT_PURPLE)
    draw.text((qx1 + 36, qy1 + 24), "CONCEPT CHECK", fill=ACCENT_PURPLE, font=fonts["small"])

    question_text = scene.get("question", "What is the result?")
    draw.text((qx1 + 30, qy1 + 65), question_text, fill=TEXT_WHITE, font=fonts["heading"])

    options = scene.get("options", ["Option 1", "Option 2"])
    correct_idx = scene.get("correct_index", 0)
    
    # Reveal answer in the second half of the scene
    dur = scene.get("duration", 6.0)
    show_answer = (t_scene > dur * 0.45)

    opt_y = qy1 + 130
    for i, opt in enumerate(options[:4]):
        ox1 = qx1 + 30
        ox2 = qx2 - 30
        oy1 = opt_y
        oy2 = opt_y + 48

        is_correct = (i == correct_idx)
        if show_answer and is_correct:
            box_fill = (22, 58, 34)
            border_col = ACCENT_GREEN
            prefix = "[✓] "
            txt_col = (255, 255, 255)
        else:
            box_fill = (28, 33, 40)
            border_col = CARD_BORDER
            prefix = f"{chr(65 + i)}. "
            txt_col = TEXT_WHITE

        draw.rounded_rectangle([ox1, oy1, ox2, oy2], radius=8, fill=box_fill, outline=border_col, width=2 if (show_answer and is_correct) else 1)
        draw.text((ox1 + 18, oy1 + 12), prefix + opt, fill=txt_col, font=fonts["sub"])

        opt_y += 58


def render_caption_bar(
    draw: ImageDraw.ImageDraw,
    narration: str,
    language: str,
    fonts: dict
):
    """Renders bottom caption bar in the target Indian language script."""
    bar_x1 = 40
    bar_x2 = WIDTH - 40
    bar_y1 = 615
    bar_y2 = 695

    # Translucent pill container
    draw.rounded_rectangle([bar_x1, bar_y1, bar_x2, bar_y2], radius=14, fill=CAPTION_BG, outline=(56, 139, 253, 120), width=1)

    # Audio speaker icon badge
    draw.rounded_rectangle([bar_x1 + 16, bar_y1 + 18, bar_x1 + 64, bar_y2 - 18], radius=6, fill=(33, 38, 45))
    draw.text((bar_x1 + 26, bar_y1 + 26), "🎙", font=fonts["small"])

    # Subtitle text
    text_x = bar_x1 + 78
    text_y = bar_y1 + 22
    
    # Simple word wrap for long narration
    words = narration.split()
    lines = []
    curr_line = []
    curr_len = 0
    max_chars = 72

    for w in words:
        if curr_len + len(w) + 1 > max_chars:
            lines.append(" ".join(curr_line))
            curr_line = [w]
            curr_len = len(w)
        else:
            curr_line.append(w)
            curr_len += len(w) + 1
    if curr_line:
        lines.append(" ".join(curr_line))

    # Render up to 2 lines
    for i, line in enumerate(lines[:2]):
        draw.text((text_x, text_y + i * 26), line, fill=TEXT_WHITE, font=fonts["caption"])


def build_concatenated_audio(scenes: List[dict], output_audio_path: str) -> bool:
    """
    Concatenates individual scene audio files into a single master audio track.
    """
    # Create FFmpeg concat list file
    list_file_path = output_audio_path + ".list.txt"
    try:
        with open(list_file_path, "w", encoding="utf-8") as f:
            for s in scenes:
                audio_path = s.get("audio_path")
                if audio_path and os.path.exists(audio_path):
                    # Escape backslashes for FFmpeg
                    clean_p = audio_path.replace("\\", "/")
                    f.write(f"file '{clean_p}'\n")

        cmd = [
            FFMPEG_EXE, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", list_file_path,
            "-c:a", "libmp3lame",
            "-qscale:a", "2",
            output_audio_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if os.path.exists(list_file_path):
            os.remove(list_file_path)
        return True
    except Exception as e:
        logger.error(f"Error concatenating audio: {e}")
        return False


def generate_srt_file(scenes: List[dict], srt_path: str):
    """Generates standard .srt subtitle file with timestamps matching scene durations."""
    def format_time(seconds: float) -> str:
        ms = int((seconds - int(seconds)) * 1000)
        s = int(seconds) % 60
        m = (int(seconds) // 60) % 60
        h = int(seconds) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    try:
        with open(srt_path, "w", encoding="utf-8") as f:
            current_t = 0.0
            for i, scene in enumerate(scenes):
                dur = scene.get("duration", 5.0)
                start_str = format_time(current_t)
                end_str = format_time(current_t + dur)
                text = scene.get("narration", "")

                f.write(f"{i + 1}\n")
                f.write(f"{start_str} --> {end_str}\n")
                f.write(f"{text}\n\n")
                current_t += dur
    except Exception as e:
        logger.warning(f"Error generating SRT file: {e}")


def export_lesson_mp4(
    lesson_plan: dict,
    output_mp4_path: str,
    progress_callback=None
) -> bool:
    """
    Main export function: Renders all animated scenes at 720p (1280x720) and
    pipes RGB24 frames into FFmpeg to produce a playable H.264 / AAC MP4 file.
    """
    scenes = lesson_plan.get("scenes", [])
    if not scenes:
        return False

    os.makedirs(os.path.dirname(output_mp4_path), exist_ok=True)
    temp_audio_path = output_mp4_path.replace(".mp4", "_audio.mp3")
    srt_path = output_mp4_path.replace(".mp4", ".srt")

    # 1. Concat master audio track
    audio_ok = build_concatenated_audio(scenes, temp_audio_path)
    if not audio_ok or not os.path.exists(temp_audio_path):
        logger.error("Failed to build master audio track")
        return False

    # 2. Generate SRT subtitle file
    generate_srt_file(scenes, srt_path)

    total_duration = sum(s.get("duration", 5.0) for s in scenes)
    total_frames = int(total_duration * FPS)
    fonts = get_fonts()
    level = lesson_plan.get("level", "beginner")
    language = lesson_plan.get("language", "en")
    lesson_title = lesson_plan.get("title", "Visual Lesson")

    # 3. Launch FFmpeg process to receive raw video frames via stdin pipe
    cmd = [
        FFMPEG_EXE, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",                     # Pipe input for video
        "-i", temp_audio_path,          # Audio track
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_mp4_path
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        current_frame = 0
        elapsed_time = 0.0

        for scene_idx, scene in enumerate(scenes):
            scene_dur = scene.get("duration", 5.0)
            scene_frames = int(scene_dur * FPS)
            stype = scene.get("type", "title_card")
            heading = scene.get("heading", "")
            narration = scene.get("narration", "")

            for f in range(scene_frames):
                t_scene = f / FPS
                overall_progress = (elapsed_time + t_scene) / max(1.0, total_duration)

                # Create 1280x720 frame image
                frame_img = Image.new("RGB", (WIDTH, HEIGHT))
                draw = ImageDraw.Draw(frame_img, "RGBA")

                # Background
                draw_background(draw)

                # Top Bar
                render_top_bar(draw, lesson_title, scene_idx, len(scenes), overall_progress, fonts)

                # Heading
                render_scene_heading(draw, heading, scene_idx, fonts)

                # Scene Components based on type
                if stype == "title_card":
                    render_title_card(draw, scene, level, language, t_scene, fonts)
                elif stype == "code_walkthrough":
                    render_code_walkthrough(draw, scene, t_scene, fonts)
                elif stype == "diagram":
                    render_diagram(draw, scene, t_scene, fonts)
                elif stype == "timeline":
                    render_timeline(draw, scene, t_scene, fonts)
                elif stype == "quiz":
                    render_quiz(draw, scene, t_scene, fonts)
                else:
                    render_title_card(draw, scene, level, language, t_scene, fonts)

                # Bottom Caption Bar
                render_caption_bar(draw, narration, language, fonts)

                # Pipe RGB bytes into FFmpeg stdin
                proc.stdin.write(frame_img.tobytes())

                current_frame += 1

            elapsed_time += scene_dur

        proc.stdin.close()
        proc.wait(timeout=60)

        # Cleanup temp audio
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        success = os.path.exists(output_mp4_path) and os.path.getsize(output_mp4_path) > 10000
        logger.info(f"Exported MP4: {output_mp4_path} ({os.path.getsize(output_mp4_path)} bytes)")
        return success

    except Exception as e:
        logger.error(f"Error during MP4 export: {e}")
        return False
