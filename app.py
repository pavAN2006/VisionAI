"""
VisionAI — AI-Powered Image Understanding
==========================================
Backend: OpenRouter API (100% Free Vision Models)
Features: 6 Analysis Modes, Auto Model Shifting, Visual Q&A Chat
"""

import re
import json
import time
import requests
import streamlit as st
from PIL import Image
import base64
import io

# ──────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VisionAI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #F8FAFC;
    background-color: #09090D !important;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="collapsedControl"] { visibility: visible !important; color: #94A3B8 !important; }
[data-testid="stSidebarCollapseButton"] { visibility: visible !important; color: #94A3B8 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #07070B !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

.brand { font-size:1.6rem; font-weight:800; letter-spacing:-0.8px; margin-bottom:2rem; }
.brand span { color:#635BFF; }

/* Nav buttons — sidebar */
div[data-testid="stSidebar"] .stButton button {
    width: 100%;
    text-align: left !important;
    background: transparent;
    border: none;
    color: #94A3B8;
    font-size: 0.95rem;
    font-weight: 500;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: all 0.15s ease;
    justify-content: flex-start;
}
div[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.04) !important;
    color: #E2E8F0 !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stSidebar"] button[kind="primary"] {
    background: rgba(99,91,255,0.12) !important;
    color: #635BFF !important;
    font-weight: 600 !important;
}

/* User profile strip */
.profile-strip {
    display:flex; align-items:center; gap:10px;
    padding:10px 12px; border-radius:8px;
    background:rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    margin-top: 2rem;
}
.avatar {
    width:32px; height:32px; border-radius:50%;
    background:#635BFF; display:flex; align-items:center;
    justify-content:center; font-weight:700; font-size:.75rem; flex-shrink:0;
}

/* ── Hero ── */
.hero-container { text-align:center; padding:4rem 1rem 2.5rem; }
.hero-title {
    font-size:3rem; font-weight:800; letter-spacing:-1.5px; margin-bottom:1rem;
    background:linear-gradient(100deg,#FFFFFF 40%,#7C6FF7);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero-sub { font-size:1.1rem; color:#64748B; max-width:540px; margin:0 auto; line-height:1.65; }

/* ── Buttons — main workspace ── */
div[data-testid="column"] .stButton button {
    background: #635BFF !important;
    border: none !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="column"] .stButton button:hover {
    background: #4F46E5 !important;
    box-shadow: 0 4px 14px rgba(99,91,255,0.35) !important;
}
.btn-ghost .stButton button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #CBD5E1 !important;
}
.btn-ghost .stButton button:hover {
    background: rgba(255,255,255,0.09) !important;
    border-color: rgba(255,255,255,0.18) !important;
    box-shadow: none !important;
}

/* ── Upload area ── */
[data-testid="stFileUploader"] { max-width:580px; margin:0 auto; }
[data-testid="stFileUploader"] > div {
    border: 2px dashed rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    background: rgba(255,255,255,0.015) !important;
    padding: 2.5rem 2rem !important;
    transition: all 0.25s ease !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: #635BFF !important;
    background: rgba(99,91,255,0.04) !important;
}

/* ── Image card ── */
.img-wrapper {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    margin-bottom: 0.5rem;
    line-height: 0;
}
.img-wrapper img { border-radius: 16px; width: 100%; display: block; }

/* ── Glass panels ── */
.glass-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.75rem 1.6rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    margin-bottom: 1.25rem;
}
.panel-heading {
    display: flex; align-items: center; gap: .6rem; margin-bottom: .7rem;
}
.panel-heading-text {
    font-size: .78rem; font-weight: 700; color: #F8FAFC;
    letter-spacing: .5px; text-transform: uppercase;
}
.panel-divider {
    height: 1px; background: rgba(255,255,255,0.07); margin-bottom: 1rem;
}
.detail-row {
    display: flex; align-items: baseline; gap: 1rem;
    padding: .6rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.detail-label {
    min-width: 110px; font-size: .78rem; font-weight: 600;
    color: #635BFF; letter-spacing: .3px; flex-shrink: 0;
}
.detail-value { font-size: .92rem; color: #E2E8F0; line-height: 1.4; }

/* ── Chat bubbles (native st.chat_message) ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.25rem 0 !important;
    gap: 0.5rem !important;
}
/* User bubble — right aligned, no avatar */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
    background: #635BFF !important;
    color: #fff !important;
    border-radius: 14px 14px 0 14px !important;
    padding: .85rem 1.15rem !important;
    max-width: 82% !important;
    box-shadow: 0 4px 12px rgba(99,91,255,0.25) !important;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {
    display: none !important;
}
/* AI bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #E2E8F0 !important;
    border-radius: 14px 14px 14px 0 !important;
    padding: .85rem 1.15rem !important;
    max-width: 88% !important;
    backdrop-filter: blur(8px) !important;
    line-height: 1.65 !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: rgba(99,91,255,0.15) !important;
    color: #635BFF !important;
    border: 1px solid rgba(99,91,255,0.3) !important;
    font-size: .65rem !important;
    font-weight: 700 !important;
}

/* ── Mode Selector Cards ── */
.mode-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    max-width: 680px;
    margin: 1.5rem auto;
}
.mode-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.mode-card:hover {
    background: rgba(99,91,255,0.08);
    border-color: rgba(99,91,255,0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,91,255,0.15);
}
.mode-card-active {
    background: rgba(99,91,255,0.12) !important;
    border-color: #635BFF !important;
    box-shadow: 0 0 0 1px #635BFF, 0 8px 24px rgba(99,91,255,0.2) !important;
}
.mode-icon { font-size: 1.8rem; margin-bottom: .5rem; display: block; }
.mode-name { font-size: .85rem; font-weight: 700; color: #E2E8F0; margin-bottom: .2rem; }
.mode-desc { font-size: .72rem; color: #64748B; line-height: 1.35; }

/* ── Code output ── */
.code-output {
    background: #0D1117;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .85rem;
    color: #E6EDF3;
    line-height: 1.6;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 1rem;
}

/* ── Color swatch ── */
.color-swatch-row {
    display: flex; align-items: center; gap: 10px;
    padding: .5rem 0; border-bottom: 1px solid rgba(255,255,255,0.04);
}
.color-dot {
    width: 28px; height: 28px; border-radius: 8px;
    border: 2px solid rgba(255,255,255,0.15);
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.color-hex {
    font-family: 'JetBrains Mono', monospace;
    font-size: .82rem; color: #A5B4FC; font-weight: 500;
}
.color-name { font-size: .85rem; color: #E2E8F0; }

/* ── Creative writing ── */
.creative-block {
    background: linear-gradient(135deg, rgba(99,91,255,0.06), rgba(139,92,246,0.04));
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    font-size: 1rem;
    line-height: 1.8;
    color: #E2E8F0;
    font-style: italic;
    margin-bottom: 1rem;
}

/* ── Object table ── */
.obj-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: .88rem;
}
.obj-table th {
    background: rgba(99,91,255,0.1);
    color: #A5B4FC;
    font-weight: 700;
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .5px;
    padding: .7rem 1rem;
    text-align: left;
    border-bottom: 1px solid rgba(99,91,255,0.2);
}
.obj-table th:first-child { border-radius: 10px 0 0 0; }
.obj-table th:last-child { border-radius: 0 10px 0 0; }
.obj-table td {
    padding: .65rem 1rem;
    color: #E2E8F0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.obj-table tr:hover td { background: rgba(255,255,255,0.02); }

/* ── Mode badge ── */
.mode-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,91,255,0.1);
    border: 1px solid rgba(99,91,255,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: .75rem;
    font-weight: 600;
    color: #A5B4FC;
    margin-bottom: 1rem;
}

/* ── Misc ── */
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 1.5rem 0; }
.page-header { font-size:1.6rem; font-weight:700; letter-spacing:-0.5px; margin-bottom:.4rem; color:#F8FAFC; }
.page-sub { font-size:.9rem; color:#64748B; margin-bottom:2rem; }
.err-strip {
    background:rgba(239,68,68,.08); border:1px solid rgba(239,68,68,.25);
    border-radius:10px; padding:.9rem 1.1rem; color:#FCA5A5; font-size:.9rem; margin-bottom:1rem;
}
.info-strip {
    background:rgba(99,91,255,.07); border:1px solid rgba(99,91,255,.2);
    border-radius:10px; padding:.9rem 1.1rem; color:#A5B4FC; font-size:.9rem; margin-bottom:1rem;
}
.hist-item {
    background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:1rem 1.25rem; margin-bottom:.75rem;
    display:flex; align-items:center; gap:.8rem; cursor:pointer; transition:background .2s;
}
.hist-item:hover { background:rgba(255,255,255,0.05); }
.setting-row {
    background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);
    border-radius:12px; padding:1.1rem 1.4rem; margin-bottom:.75rem;
}
.setting-label { font-size:.95rem; font-weight:600; color:#E2E8F0; margin-bottom:.2rem; }
.setting-sub { font-size:.82rem; color:#64748B; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# OpenRouter config
# ──────────────────────────────────────────────────────────────────────
OPENROUTER_BASE = "https://openrouter.ai/api/v1/chat/completions"

# 100% Free vision-capable models on OpenRouter (tried in order, falls back on rate limit/error)
MODELS_LIST = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "inclusionai/ling-3.0-flash-vl:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "dots-studio/dots-3-note-preview:free",
    "nex-agi/nex-n2.5-mini:free",
]

# Last-resort auto-router — OpenRouter picks the best available free model
FALLBACK_MODEL = "openrouter/auto"

# ──────────────────────────────────────────────────────────────────────
# Analysis Modes
# ──────────────────────────────────────────────────────────────────────
ANALYSIS_MODES = {
    "describe": {
        "icon": "✨",
        "name": "Describe",
        "desc": "Full scene description & details",
        "prompt": """\
You are VisionAI, an expert image understanding assistant.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the paragraph description.

Provide your response in this EXACT order and format:

## ✨ AI Description
Write 1–2 detailed, natural paragraphs describing the complete scene, subjects, actions, colors, setting, lighting, and any visible text.

## 🔍 Detected Details
- **Subjects:** Key people, animals, or objects
- **Action:** Primary action or activities happening
- **Location:** Apparent setting and place
- **Environment:** Background and surroundings
- **Mood:** Visual atmosphere and lighting style

Rules:
- Describe only what is clearly visible in the image.
- Do not repeat information between the paragraph and details.
- Never output reasoning or analysis process.""",
    },
    "ocr": {
        "icon": "📝",
        "name": "Extract Text",
        "desc": "OCR — read text from images",
        "prompt": """\
You are VisionAI OCR, an expert text extraction system.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the extracted text.

Your task: Extract ALL visible text from this image exactly as written.

## 📝 Extracted Text
Reproduce every piece of text visible in the image, preserving:
- Original line breaks and layout structure
- Headers, labels, captions, signs, watermarks
- Any handwritten text (note if confidence is low)
- Numbers, dates, codes, URLs

## 📋 Text Summary
- **Total text regions:** Count of distinct text areas found
- **Languages detected:** What language(s) the text appears to be in
- **Text type:** (Printed / Handwritten / Mixed / Digital)
- **Readability:** (Clear / Partially obscured / Difficult)

Rules:
- If no text is found, state "No readable text detected in this image."
- For partially visible text, use [...] for unreadable portions.
- Preserve original formatting as closely as possible.""",
    },
    "objects": {
        "icon": "🎯",
        "name": "Detect Objects",
        "desc": "Identify & count all objects",
        "prompt": """\
You are VisionAI Object Detector, an expert visual object identification system.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the object list.

Your task: Identify and catalog every distinct object visible in this image.

## 🎯 Detected Objects

Provide a structured list. For EACH object include:
| Object | Count | Position | Size | Confidence |
|--------|-------|----------|------|------------|

Where:
- **Object**: Name of the object
- **Count**: How many instances (1, 2, 3+, etc.)
- **Position**: Location in frame (top-left, center, bottom-right, etc.)
- **Size**: Relative to frame (small, medium, large, dominant)
- **Confidence**: How certain (high, medium, low)

## 📊 Summary
- **Total unique objects:** count
- **Total items detected:** count
- **Scene complexity:** (Simple / Moderate / Complex / Very Complex)
- **Primary subject:** The most prominent object

Rules:
- List objects from most prominent to least prominent.
- Include background objects and partial objects at edges.
- Be specific: "golden retriever" not just "dog", "oak tree" not just "tree".""",
    },
    "colors": {
        "icon": "🎨",
        "name": "Color & Style",
        "desc": "Palette, composition & aesthetics",
        "prompt": """\
You are VisionAI Style Analyst, an expert in visual aesthetics and color theory.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the color analysis.

Your task: Analyze the visual design, color palette, and artistic style of this image.

## 🎨 Color Palette
List the 5-8 most dominant colors in this image. For each:
- **Color name** (e.g., "Warm Coral", "Deep Navy")
- **Hex code** (e.g., #FF6B6B)
- **Percentage** — approximate coverage in image (e.g., ~25%)
- **Role** — what it represents (background, accent, subject, shadow, etc.)

## 🖌️ Visual Style
- **Art style:** (Photograph / Illustration / Digital Art / Painting / Screenshot / etc.)
- **Composition:** (Rule of thirds / Centered / Symmetrical / Dynamic / etc.)
- **Lighting:** (Natural / Studio / Dramatic / Flat / Golden hour / etc.)
- **Contrast:** (High / Medium / Low)
- **Mood/Tone:** (Warm / Cool / Neutral / Vibrant / Muted)
- **Texture:** (Smooth / Rough / Glossy / Matte / Mixed)

## 💡 Design Notes
One paragraph describing how the colors and composition work together, and any notable design choices.

Rules:
- Be specific with color names and hex codes.
- Percentages should roughly add up to 100%.
- If it's a photo, describe the photography style.""",
    },
    "code": {
        "icon": "💻",
        "name": "Code from Image",
        "desc": "Convert UI screenshots to code",
        "prompt": """\
You are VisionAI Code Generator, an expert at converting visual designs into code.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the code output.

Your task: Convert this UI screenshot into clean, functional HTML and CSS code.

## 💻 Generated Code

Provide a COMPLETE, single HTML file with embedded CSS that recreates this UI. Requirements:
- Use semantic HTML5 elements
- Use modern CSS (Flexbox/Grid)
- Include responsive design basics
- Use a clean color palette matching the screenshot
- Add appropriate padding, margins, and border-radius
- Include hover states for interactive elements
- Use system fonts or Google Fonts
- Make it pixel-perfect to the original as possible

```html
<!-- Your complete HTML file here -->
```

## 📋 Implementation Notes
- **Framework suggestion:** What framework would be best for this UI
- **Components identified:** List of UI components found
- **Responsive notes:** How the layout should adapt to mobile

Rules:
- Output ONLY valid, runnable HTML/CSS.
- Do not use external CSS frameworks unless the screenshot clearly uses one.
- Include realistic placeholder content matching what's in the image.""",
    },
    "creative": {
        "icon": "✍️",
        "name": "Creative Writing",
        "desc": "Stories & poems from images",
        "prompt": """\
You are VisionAI Creative Writer, a masterful storyteller and poet.

CRITICAL INSTRUCTIONS:
- DO NOT write any "Thinking Process:", thought tags, or meta-commentary.
- Start IMMEDIATELY with the creative writing.

Your task: Create an original, evocative piece of creative writing inspired by this image.

## ✍️ Creative Piece

Write ONE of the following (choose whichever best fits the image's mood):
- A short story (200-300 words) with vivid imagery
- A poem (12-20 lines) with strong rhythm and metaphor
- A narrative vignette capturing a frozen moment in time

The writing should:
- Capture the mood, atmosphere, and emotion of the image
- Use sensory details (sight, sound, smell, touch, taste)
- Have a compelling opening line
- Feel literary and polished, not generic

## 🎭 About This Piece
- **Form:** (Short Story / Poem / Vignette / Micro-Fiction)
- **Mood:** The emotional tone captured
- **Inspiration:** What element of the image sparked the writing

Rules:
- Be original and creative — avoid clichés.
- Match the tone to the image (dark image = darker writing, bright = uplifting).
- The writing should stand on its own as a quality piece.""",
    },
}

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────
def validate_image(f):
    """Return (ok, error_msg, PIL_image)."""
    if f is None:
        return False, "No file.", None
    valid_ext = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif")
    if not f.name.lower().endswith(valid_ext):
        return False, f"Unsupported format. Supported: {', '.join(valid_ext)}", None
    try:
        b = f.getvalue()
        if not b:
            return False, "File is empty.", None
        img = Image.open(io.BytesIO(b))
        img.verify()
        return True, "", Image.open(io.BytesIO(b))
    except Exception:
        return False, "Corrupted or unreadable file.", None


def to_b64(img: Image.Image) -> str:
    """Resize to max 512px and encode as JPEG base64."""
    buf = io.BytesIO()
    rgb = img.convert("RGB")
    rgb.thumbnail((512, 512))
    rgb.save(buf, "JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()


def parse_analysis(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split AI response into (description, [(label, value), ...])."""
    # 1. Strip XML think blocks if present
    clean_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # 2. Strip explicit 'Thinking Process:' preamble if present
    clean_text = re.sub(r"(?is)^.*?Thinking Process:.*?(?=(##\s*✨|##\s*🔍|✨\s*AI|\n\n\b[A-Z]))", "", clean_text)

    # 3. If '## ✨ AI Description' exists, discard any lingering preamble before it
    desc_match = re.search(r"(?:##\s*)?(?:✨|\u2728)?\s*AI Description\s*:?", clean_text, flags=re.IGNORECASE)
    if desc_match:
        clean_text = clean_text[desc_match.end():]

    # Clean leading headings from description
    for heading in ["## ✨ AI Description", "## \u2728 AI Description", "✨ AI Description", "AI Description:"]:
        clean_text = clean_text.replace(heading, "").strip()

    desc = clean_text.strip()
    details: list[tuple[str, str]] = []

    split_markers = [
        "## 🔍 Detected Details",
        "## \U0001f50d Detected Details",
        "### 🔍 Detected Details",
        "🔍 Detected Details",
        "## Detected Details",
        "Detected Details:",
        "## Key Details",
        "Key Details:",
    ]
    for marker in split_markers:
        if marker in desc:
            parts = desc.split(marker, 1)
            desc = parts[0].strip()
            for line in parts[1].splitlines():
                line = line.strip()
                m = re.match(r"[-*•]?\s*\*{0,2}([^:*]+)\*{0,2}:\s*(.+)", line)
                if m:
                    details.append((m.group(1).strip(), m.group(2).strip()))
            break

    return desc, details


def or_chat(messages: list, token: str) -> str:
    """
    Call OpenRouter with automatic model fallback.
    Tries each free vision model in MODELS_LIST in round-robin order starting
    from session_state.model_idx. Returns assistant text on success.
    Falls back to openrouter/auto as last resort.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://visionai.streamlit.app",
        "X-Title": "VisionAI Studio",
    }

    errors_log = []
    # Try all hardcoded models first
    for _ in range(len(MODELS_LIST)):
        model_id = MODELS_LIST[st.session_state.model_idx]
        st.session_state.model_idx = (st.session_state.model_idx + 1) % len(MODELS_LIST)

        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": 2000,
        }
        for attempt in range(2):
            try:
                resp = requests.post(
                    OPENROUTER_BASE,
                    headers=headers,
                    json=payload,
                    timeout=90,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        err_msg = data["error"].get("message", str(data["error"]))
                        errors_log.append(f"{model_id}: {err_msg}")
                        break

                    choices = data.get("choices")
                    if not choices:
                        errors_log.append(f"{model_id}: No choices returned")
                        break

                    msg_obj = choices[0].get("message", {})
                    content = (
                        msg_obj.get("content")
                        or msg_obj.get("reasoning")
                        or msg_obj.get("reasoning_content")
                        or ""
                    )
                    if content and content.strip():
                        # Store which model responded
                        st.session_state.last_model = model_id
                        return content.strip()
                    errors_log.append(f"{model_id}: Empty response text")
                    break
                elif resp.status_code in (429, 503):
                    if attempt == 0:
                        time.sleep(1.5)
                        continue
                    errors_log.append(f"{model_id}: Rate limited (429/503)")
                    break
                else:
                    try:
                        err_data = resp.json()
                        msg = err_data.get("error", {}).get("message", resp.text)
                    except Exception:
                        msg = resp.text
                    errors_log.append(f"{model_id} (error {resp.status_code}): {msg}")
                    break
            except requests.exceptions.Timeout:
                errors_log.append(f"{model_id}: Timed out")
                break
            except Exception as e:
                errors_log.append(f"{model_id}: {str(e)}")
                break

    # Last resort: try the auto-router
    try:
        payload = {
            "model": FALLBACK_MODEL,
            "messages": messages,
            "max_tokens": 2000,
        }
        resp = requests.post(OPENROUTER_BASE, headers=headers, json=payload, timeout=90)
        if resp.status_code == 200:
            data = resp.json()
            choices = data.get("choices")
            if choices:
                msg_obj = choices[0].get("message", {})
                content = msg_obj.get("content") or msg_obj.get("reasoning") or ""
                if content and content.strip():
                    st.session_state.last_model = FALLBACK_MODEL
                    return content.strip()
        errors_log.append(f"{FALLBACK_MODEL}: Failed ({resp.status_code})")
    except Exception as e:
        errors_log.append(f"{FALLBACK_MODEL}: {str(e)}")

    formatted_errors = "\n• " + "\n• ".join(errors_log)
    raise RuntimeError(
        f"All models failed:\n{formatted_errors}\n\n"
        "Please check your OpenRouter API key and settings at openrouter.ai/settings/privacy."
    )


# ──────────────────────────────────────────────────────────────────────
# Session state defaults
# ──────────────────────────────────────────────────────────────────────
DEFAULTS: dict = {
    "page":        "Workspace",
    "model_idx":   0,
    "last_model":  "",
    "img_hash":    None,
    "img_bytes":   None,
    "img_name":    None,
    "img_size":    0,
    "analysis":    None,
    "mode":        None,
    "messages":    [],
    "pending":     None,
    "history":     [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="brand">Vision<span>AI</span></p>', unsafe_allow_html=True)

    for label, icon in [("Workspace","✦"), ("History","🕒"), ("Saved","🔖"), ("Settings","⚙️")]:
        is_active = st.session_state.page == label
        if st.button(f"{icon}  {label}", key=f"nav_{label}", type="primary" if is_active else "secondary"):
            st.session_state.page = label
            st.rerun()

    st.markdown("""
    <div class="profile-strip">
        <div class="avatar">VS</div>
        <div>
            <div style="font-size:.85rem;font-weight:600;color:#E2E8F0;">Your Space</div>
            <div style="font-size:.75rem;color:#64748B;">Free Plan</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# API token guard
# ──────────────────────────────────────────────────────────────────────
_api_token = (
    st.secrets.get("openrouter_api_key", "")
    or st.secrets.get("openrouter_key", "")
    or st.secrets.get("openrouter_token", "")
)
if not _api_token:
    st.markdown(
        '<div class="err-strip">⚠️ <b>OpenRouter API key missing.</b> '
        'Add <code>openrouter_api_key = "sk-or-v1-..."</code> to <code>.streamlit/secrets.toml</code>.<br><br>'
        '👉 Get a 100% free key (no credit card needed) at <a href="https://openrouter.ai/keys" target="_blank" style="color:#A5B4FC;">openrouter.ai/keys</a></div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ══════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════

# ── HISTORY ───────────────────────────────────────────────────────────
if st.session_state.page == "History":
    st.markdown('<div class="page-header">🕒 History</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Your recent image analysis sessions.</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            mode_info = ANALYSIS_MODES.get(item.get("mode", "describe"), ANALYSIS_MODES["describe"])
            st.markdown(f"""
            <div class="hist-item">
                <div style="font-size:1.4rem;">{mode_info['icon']}</div>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:.9rem;color:#E2E8F0;">{item.get('name', 'Unknown')}</div>
                    <div style="font-size:.8rem;color:#64748B;">{mode_info['name']} · {item.get('msg_count', 0)} messages</div>
                </div>
                <div style="font-size:.78rem;color:#475569;">{item.get('time', '')}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🕒</div>
            <div style="font-weight:600;font-size:1rem;color:#94A3B8;margin-bottom:.4rem;">No history yet</div>
            <div style="font-size:.85rem;color:#475569;">Analyze an image and it will appear here.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="info-strip" style="margin-top:1rem;">Session history is stored locally per browser session.</div>', unsafe_allow_html=True)
    st.stop()

# ── SAVED ─────────────────────────────────────────────────────────────
if st.session_state.page == "Saved":
    st.markdown('<div class="page-header">🔖 Saved</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Bookmarked analyses and conversations.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:4rem 1rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">🔖</div>
        <div style="font-weight:600;font-size:1rem;color:#94A3B8;margin-bottom:.4rem;">Nothing saved yet</div>
        <div style="font-size:.85rem;color:#475569;">Bookmark an analysis result to find it here later.</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── SETTINGS ──────────────────────────────────────────────────────────
if st.session_state.page == "Settings":
    st.markdown('<div class="page-header">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Application preferences.</div>', unsafe_allow_html=True)
    current_model = MODELS_LIST[st.session_state.model_idx % len(MODELS_LIST)]

    # Models info
    models_display = ", ".join([m.split("/")[-1].replace(":free", "") for m in MODELS_LIST])
    modes_display = " · ".join([f"{v['icon']} {v['name']}" for v in ANALYSIS_MODES.values()])

    for label, value, sub in [
        ("🤖 AI Backend",     "OpenRouter (100% Free Vision Models)",     f"Auto-shifts across {len(MODELS_LIST)} free models + auto-router fallback"),
        ("🎯 Current Model",  current_model,                              "Round-robin across free vision models"),
        ("📊 Model Pool",     f"{len(MODELS_LIST)} models",              models_display),
        ("🧩 Analysis Modes", f"{len(ANALYSIS_MODES)} modes",            modes_display),
        ("🎨 Theme",          "Dark Mode",                                "Default appearance"),
        ("📁 Max Upload",     "10 MB",                                    "Set in config.toml"),
        ("🌐 Language",       "English",                                  "Interface language"),
    ]:
        st.markdown(f"""
        <div class="setting-row">
            <div class="setting-label">{label}</div>
            <div style="font-size:.9rem;color:#7C6FF7;margin-bottom:.15rem;">{value}</div>
            <div class="setting-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, _, __ = st.columns([1, 1, 2])
    with col1:
        if st.button("🗑️ Clear Session"):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════
# PAGE: WORKSPACE
# ══════════════════════════════════════════════════════════════════════

# ── State 1: No image ─────────────────────────────────────────────────
if st.session_state.img_hash is None:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Understand any image with AI</div>
        <div class="hero-sub">Upload an image and let VisionAI analyze, describe, extract text, detect objects, and answer questions about it.</div>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("drop", type=["jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "gif"], label_visibility="collapsed")
    if uploaded:
        ok, err, img = validate_image(uploaded)
        if ok:
            st.session_state.img_hash  = hash(uploaded.getvalue())
            st.session_state.img_bytes = uploaded.getvalue()
            st.session_state.img_name  = uploaded.name
            st.session_state.img_size  = len(uploaded.getvalue())
            st.session_state.analysis  = None
            st.session_state.mode      = None
            st.session_state.messages  = []
            st.rerun()
        else:
            st.error(f"⚠️ {err}")
    st.stop()

# ── State 2+: Image is in session ─────────────────────────────────────
img_pil = Image.open(io.BytesIO(st.session_state.img_bytes))

# "New Image" button top-right
st.markdown('<div class="btn-ghost" style="text-align: right; margin-bottom: 1rem;">', unsafe_allow_html=True)
if st.button("↩ New Image"):
    # Save to history before clearing
    if st.session_state.analysis:
        import datetime
        st.session_state.history.append({
            "name": st.session_state.img_name,
            "mode": st.session_state.mode or "describe",
            "msg_count": len(st.session_state.messages),
            "time": datetime.datetime.now().strftime("%I:%M %p"),
        })
    for k, v in DEFAULTS.items():
        if k != "history":  # preserve history
            st.session_state[k] = v
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Centered image display
st.image(img_pil, use_container_width=True)
size_kb = st.session_state.img_size / 1024
st.markdown(
    f'<p style="text-align:center;color:#475569;font-size:.82rem;margin-top:.3rem;margin-bottom:1.5rem;">'
    f'{st.session_state.img_name} · {size_kb:.1f} KB · {img_pil.width}×{img_pil.height}</p>',
    unsafe_allow_html=True,
)

# ── State 2: Awaiting analysis — MODE SELECTOR ───────────────────────
if st.session_state.analysis is None:
    st.markdown("""
    <div style="text-align:center;margin-bottom:0.5rem;">
        <span style="font-size:1.1rem;font-weight:700;color:#E2E8F0;">Choose Analysis Mode</span>
        <p style="font-size:.85rem;color:#64748B;margin-top:.3rem;">Select how you want VisionAI to analyze this image</p>
    </div>""", unsafe_allow_html=True)

    # Create 2 rows of 3 columns for mode cards
    mode_keys = list(ANALYSIS_MODES.keys())

    row1_cols = st.columns(3)
    row2_cols = st.columns(3)
    all_cols = row1_cols + row2_cols

    for idx, mode_key in enumerate(mode_keys):
        mode = ANALYSIS_MODES[mode_key]
        with all_cols[idx]:
            if st.button(
                f"{mode['icon']}\n\n**{mode['name']}**\n\n{mode['desc']}",
                key=f"mode_{mode_key}",
                use_container_width=True,
            ):
                st.session_state.mode = mode_key
                with st.spinner(f"{mode['icon']} Analyzing with {mode['name']}…"):
                    try:
                        b64 = to_b64(img_pil)
                        resp = or_chat(
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                                    {"type": "text", "text": mode["prompt"]}
                                ]
                            }],
                            token=_api_token,
                        )
                        st.session_state.analysis = resp
                        # Save to history
                        import datetime
                        st.session_state.history.append({
                            "name": st.session_state.img_name,
                            "mode": mode_key,
                            "msg_count": 0,
                            "time": datetime.datetime.now().strftime("%I:%M %p"),
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(f"API Error: {e}")
    st.stop()

# ── State 3+: Analysis ready ──────────────────────────────────────────
current_mode = st.session_state.mode or "describe"
mode_info = ANALYSIS_MODES.get(current_mode, ANALYSIS_MODES["describe"])

# Mode badge + model chip
model_display = st.session_state.get("last_model", "").split("/")[-1].replace(":free", "") if st.session_state.get("last_model") else "AI"
st.markdown(
    f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">'
    f'<span class="mode-badge">{mode_info["icon"]} {mode_info["name"]}</span>'
    f'<span style="font-size:.72rem;color:#475569;">via {model_display}</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── MODE-SPECIFIC RENDERING ──────────────────────────────────────────
if current_mode == "describe":
    # Original glass-panel rendering
    desc_text, detail_rows = parse_analysis(st.session_state.analysis)

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">✨</span>
            <span class="panel-heading-text">AI Description</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(desc_text)

    if detail_rows:
        rows_html = "".join(
            f'<div class="detail-row">'
            f'<span class="detail-label">{lbl}</span>'
            f'<span class="detail-value">{val}</span>'
            f'</div>'
            for lbl, val in detail_rows
        )
        st.markdown(f"""
        <div class="glass-panel" style="margin-top:.75rem;">
            <div class="panel-heading">
                <span style="font-size:1.1rem;">🔍</span>
                <span class="panel-heading-text">Detected Details</span>
            </div>
            <div class="panel-divider"></div>
            {rows_html}
        </div>""", unsafe_allow_html=True)

elif current_mode == "ocr":
    # Clean think blocks from OCR output
    clean = re.sub(r"<think>.*?</think>", "", st.session_state.analysis, flags=re.DOTALL).strip()

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">📝</span>
            <span class="panel-heading-text">Extracted Text</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(clean)

elif current_mode == "objects":
    clean = re.sub(r"<think>.*?</think>", "", st.session_state.analysis, flags=re.DOTALL).strip()

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">🎯</span>
            <span class="panel-heading-text">Detected Objects</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(clean)

elif current_mode == "colors":
    clean = re.sub(r"<think>.*?</think>", "", st.session_state.analysis, flags=re.DOTALL).strip()

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">🎨</span>
            <span class="panel-heading-text">Color & Style Analysis</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(clean)

elif current_mode == "code":
    clean = re.sub(r"<think>.*?</think>", "", st.session_state.analysis, flags=re.DOTALL).strip()

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">💻</span>
            <span class="panel-heading-text">Generated Code</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(clean)

elif current_mode == "creative":
    clean = re.sub(r"<think>.*?</think>", "", st.session_state.analysis, flags=re.DOTALL).strip()

    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">✍️</span>
            <span class="panel-heading-text">Creative Writing</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    # Wrap creative content in styled block
    st.markdown(f'<div class="creative-block">', unsafe_allow_html=True)
    st.markdown(clean)
    st.markdown('</div>', unsafe_allow_html=True)

# Re-analyze with different mode
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:.82rem;color:#64748B;margin-bottom:.5rem;">Try another mode on this image:</p>',
    unsafe_allow_html=True,
)
reanalyze_cols = st.columns(len(ANALYSIS_MODES))
for idx, (mode_key, mode) in enumerate(ANALYSIS_MODES.items()):
    with reanalyze_cols[idx]:
        disabled = mode_key == current_mode
        if st.button(
            f"{mode['icon']} {mode['name']}",
            key=f"reanalyze_{mode_key}",
            disabled=disabled,
            use_container_width=True,
        ):
            st.session_state.mode = mode_key
            st.session_state.analysis = None
            st.session_state.messages = []
            with st.spinner(f"{mode['icon']} Re-analyzing with {mode['name']}…"):
                try:
                    b64 = to_b64(img_pil)
                    resp = or_chat(
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                                {"type": "text", "text": mode["prompt"]}
                            ]
                        }],
                        token=_api_token,
                    )
                    st.session_state.analysis = resp
                    import datetime
                    st.session_state.history.append({
                        "name": st.session_state.img_name,
                        "mode": mode_key,
                        "msg_count": 0,
                        "time": datetime.datetime.now().strftime("%I:%M %p"),
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"API Error: {e}")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Chat history
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        st.markdown(msg["text"])

# Chat input (must be outside all columns to anchor at bottom)
prompt_in = st.chat_input("Ask anything about this image…")
if prompt_in:
    st.session_state.pending = prompt_in

# Process any pending message
if st.session_state.pending and st.session_state.img_bytes:
    user_text = st.session_state.pending
    st.session_state.pending = None
    st.session_state.messages.append({"role": "user", "text": user_text})

    with st.spinner("Generating response…"):
        b64 = to_b64(img_pil)
        # Flatten conversation history into a single prompt string
        prompt = f"Context (your previous {mode_info['name']} analysis of the image):\n{st.session_state.analysis}\n\n"
        if len(st.session_state.messages) > 1:
            prompt += "Conversation history:\n"
            for m in st.session_state.messages[:-1]:
                speaker = "User" if m["role"] == "user" else "Assistant"
                prompt += f"{speaker}: {m['text']}\n"

        latest_user_text = st.session_state.messages[-1]["text"]
        prompt += f"\nUser: {latest_user_text}\nPlease answer the user's question based on the image and the {mode_info['name']} analysis context above."

        # Send a SINGLE message containing the image and the flattened text
        history = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        try:
            ai_resp = or_chat(history, token=_api_token)
            st.session_state.messages.append({"role": "assistant", "text": ai_resp})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "text": f"❌ {e}"})
    st.rerun()
