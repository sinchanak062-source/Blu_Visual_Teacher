<<<<<<< HEAD
# Blu Visual Teacher 🎬
> **Offline Local-First Engine that turns any typed concept into short, narrated, animated 720p visual lessons in English and Indian languages (Hindi, Tamil, Telugu, Marathi, Bengali).**
> Built for the **Blu Visual Teacher Hackathon (2026)**.

---

## 🌟 Overview & Key Capabilities

Blu Visual Teacher takes an educational concept (e.g., *"How does a Python loop work?"* or *"Binary Search"*) and automatically produces a **30–90 second animated video lesson** with:
1. **Animated Visual Components**: Title Cards, macOS/VSCode Code Walkthroughs with highlighted line focus, Connected Flow Diagrams with directional arrows, Milestones Timelines, and Concept Check Quizzes.
2. **Synchronized Multilingual Voice-over**: English (Indian Accent), Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), and Bengali (বাংলা).
3. **Burned-In Native Script Captions**: Devanagari, Tamil, Telugu, and Latin scripts, plus downloadable `.srt` files.
4. **Key Design Rule Strictly Followed**: **Voice-over audio sets each scene's duration**. Audio is synthesized first; each scene lasts exactly `audio_duration + pause` to eliminate drift between visuals, subtitles, and narration.
5. **100% Offline Resilience**: If Wi-Fi is switched off or Ollama is offline, the system never breaks. It seamlessly falls back to local verified lessons and structured semantic template generation.
6. **720p MP4 Export**: High-quality `1280x720` H.264 video with AAC audio rendered in seconds on a standard CPU laptop.

---

## 📐 Five Core Stages

| Stage | Feature | Implementation Details | Done Criteria |
|---|---|---|---|
| **1. Concept Input** | Web Interface | Topic input, difficulty level (Beginner/Intermediate), language picker, duration target, and quick topic chips. | Topic, level, and language reach backend API. |
| **2. Lesson Planner** | Local LLM / Offline Fallback | Queries local Ollama (`llama3.2`, `mistral`, `phi3`) or smart offline generator. Validates against JSON Schema. | Strict schema check passed; guaranteed never to crash. |
| **3. Visual Engine** | Browser Player & Canvas | Reusable animated components for 5 scene types: Title Card, Code Walkthrough, Diagram, Timeline, Quiz. | Play, pause, seek, replay, and live step headings. |
| **4. Multilingual Narration** | Audio & Subtitle Sync | Voice-over sets scene length (`audio_dur + pause`). Native script captions in Devanagari, Tamil, etc. | Spoken narration, captions, and visual scene stay in lockstep. |
| **5. MP4 Export** | FFmpeg 720p Pipeline | Combines animated 1280x720 frames, master audio, and captions into an H.264/AAC MP4. | Playable 720p MP4 and `.srt` file downloadable. |

---

## 🎁 Bonus Features Included

- **More Indian Languages**: English, Hindi, Tamil, Telugu, Marathi, Bengali.
- **Instant Re-voicing**: Switch languages on a completed lesson without re-planning the scenes.
- **Voice Choice & Speed Control**: Male and Female voices with 0.9x, 1.0x, and 1.15x speed controls.
- **Teacher Scene Editor (Edit Before Render)**: Edit headings, narration text, code lines, or diagram items, and re-generate audio for that specific scene.
- **Lesson Cache**: Automatically caches completed lessons by topic, language, and version to prevent redundant compute.
- **Telemetry & Footprint Monitor**: Displays stage-by-stage timing (LLM Plan time, TTS time, Render time) and system RAM usage.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14 on Windows)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 1. Installation
Clone the repository or navigate to the directory:
```bash
cd blu-visual-teacher
pip install -r requirements.txt
```

### 2. Launching the Application
On Windows, double-click **`run.bat`** or run:
```bash
python backend/server.py
```
Open your browser at:
👉 **`http://127.0.0.1:5000`**

---

## 🧪 Testing with Wi-Fi Switched Off (Offline Demo)

The entire application runs **100% offline**:
1. Turn off your Wi-Fi or disconnect Ethernet.
2. In the web interface, type any concept (e.g. *"How a Python loop works"* or *"Photosynthesis"*).
3. Select your desired language (e.g., Hindi or English) and click **"⚡ Generate Lesson"**.
4. The system will:
   - Use the offline semantic planner (schema-validated)
   - Synthesize acoustic voice narration locally
   - Animate the visual scenes with synchronized captions
   - Export a playable 720p MP4 via local FFmpeg!

---

## 📁 Pre-Generated Benchmark Lessons (Judge Showcase)

The project includes ready-to-play, verified 720p MP4 lessons located in the `pregenerated/` directory:

| Filename | Topic | Language | Duration | Resolution |
|---|---|---|---|---|
| `python_loop_en.mp4` | Python Loops | English (Indian Accent) | 34.6s | 1280x720 H.264 |
| `python_loop_hi.mp4` | पायथन लूप कैसे काम करता है | Hindi (हिंदी) | 32.7s | 1280x720 H.264 |
| `binary_search_en.mp4` | Understanding Binary Search | English | 39.3s | 1280x720 H.264 |
| `binary_search_hi.mp4` | बाइनरी सर्च को समझें | Hindi (हिंदी) | 37.4s | 1280x720 H.264 |

Click any benchmark card in the web UI for instant offline playback.

---

## 💻 Tested Laptop Specs & Footprint

- **OS**: Windows 11 64-bit
- **CPU**: Intel Core i5 / AMD Ryzen (Tested in CPU-only mode, no GPU required)
- **RAM**: 8 GB – 16 GB RAM
- **Disk Footprint**: ~45 MB for core engine & binaries
- **Generation Speed**:
  - LLM Planning: ~0.1s (offline) / 1.5s (Ollama 1B/3B)
  - Narration & Sync: ~0.8s
  - 720p 24fps MP4 Video Render: ~14.9s for a 35-second lesson (~2.3x realtime)

---

## 📜 Models, Voices & Open-Source Licences

All models, voices, libraries, and assets used in Blu Visual Teacher are compliant with hackathon licensing requirements:

| Component | Asset / Model | Licence | Notes |
|---|---|---|---|
| **Local LLM** | Ollama (Llama 3.2 1B / 3B) | Meta Llama 3.2 Community License / MIT | Runs locally on CPU |
| **Planner Fallback** | Blu Synthesizer Engine | MIT License | Rule-based offline generator |
| **TTS Engine** | Kokoro-ONNX / Edge-TTS / Acoustic Synth | Apache 2.0 / MIT | Multi-lingual CPU speech |
| **Video Compositor** | FFmpeg 7.1 Essentials Build | LGPL / GPL v3 | Bundled static binary |
| **Typography** | Nirmala UI / Noto Sans | SIL Open Font License / Microsoft Standard | Indian scripts support |
| **Web Framework** | Flask & Flask-CORS | BSD-3-Clause | Lightweight API server |
| **Imaging Engine** | Pillow (PIL Fork) | HPND License | Frame rendering |

---

## 📂 Repository Structure

```
blu-visual-teacher/
├── backend/
│   ├── server.py              # Flask HTTP API server
│   ├── planner.py             # LLM Planner & offline fallback synthesizer
│   ├── schema.py              # JSON Schema validator for lesson plans
│   ├── tts_engine.py          # Multilingual narration & duration-sync engine
│   ├── video_renderer.py      # 720p H.264 frame renderer & FFmpeg exporter
│   ├── lesson_cache.py        # Lesson caching mechanism
│   ├── generate_samples.py    # Script to pre-generate benchmark lessons
│   └── samples/
│       └── sample_lessons.py  # Curated reference lessons in EN, HI, TA, TE
├── frontend/
│   ├── index.html             # Responsive Web UI
│   ├── styles.css             # Polished dark theme, CSS animations
│   └── app.js                 # Frontend Visual Engine & player logic
├── pregenerated/              # Ready-to-play 720p MP4 lessons for judges
│   ├── python_loop_en.mp4
│   ├── python_loop_hi.mp4
│   ├── binary_search_en.mp4
│   └── binary_search_hi.mp4
├── static/
│   ├── cache/                 # Cached audio & lesson plans
│   └── generated/             # Exported MP4s & SRT subtitles
├── run.bat                    # One-click Windows startup script
├── requirements.txt           # Python dependencies
└── README.md                  # Complete documentation & licence breakdown
```
=======
# Blu_Visual_Teacher
>>>>>>> 0b48c231b3552a654b0dc2591607dc85f7206b96
