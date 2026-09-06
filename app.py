"""
VisionAI — AI-Powered Image Understanding
=========================================
Model: deepseek-ai/DeepSeek-V4-Flash-Vision-Exp
"""

import re
import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient
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
div[data-testid="stSidebar"] .nav-active .stButton button {
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
# Helpers
# ──────────────────────────────────────────────────────────────────────
def validate_image(f):
    """Return (ok, error_msg, PIL_image)."""
    if f is None:
        return False, "No file.", None
    if not f.name.lower().endswith((".jpg", ".jpeg", ".png")):
        return False, "Only JPG / PNG supported.", None
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
    """Resize to max 1024px and encode as JPEG base64."""
    buf = io.BytesIO()
    rgb = img.convert("RGB")
    rgb.thumbnail((1024, 1024))
    rgb.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def parse_analysis(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split AI response into (description, [(label, value), ...])."""
    desc = text
    details: list[tuple[str, str]] = []

    split_markers = [
        "## 🔍 Detected Details",
        "## \U0001f50d Detected Details",
        "🔍 Detected Details",
    ]
    for marker in split_markers:
        if marker in text:
            parts = text.split(marker, 1)
            desc = parts[0].strip()
            for line in parts[1].splitlines():
                line = line.strip()
                m = re.match(r"[-*]?\s*\*{0,2}([^:*]+)\*{0,2}:\s*(.+)", line)
                if m:
                    details.append((m.group(1).strip(), m.group(2).strip()))
            break

    # Strip the description heading if the model echoed it
    for heading in ["## ✨ AI Description", "## \u2728 AI Description", "✨ AI Description"]:
        desc = desc.replace(heading, "").strip()

    return desc, details


def hf_chat(messages: list) -> str:
    """Call the HF inference API and return the assistant text."""
    token = st.secrets.get("hf_token", "")
    if not token:
        raise ValueError("hf_token not found in secrets.toml")
    client = InferenceClient(api_key=token)
    r = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V4-Flash-Vision-Exp",
        messages=messages,
        max_tokens=700,
    )
    return r.choices[0].message.content

# ──────────────────────────────────────────────────────────────────────
# Session state defaults
# ──────────────────────────────────────────────────────────────────────
DEFAULTS: dict = {
    "page":      "Workspace",
    "img_hash":  None,
    "img_bytes": None,
    "img_name":  None,
    "img_size":  0,
    "analysis":  None,
    "messages":  [],
    "pending":   None,
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
        st.markdown(f'<div class="{"nav-active" if is_active else ""}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{label}"):
            st.session_state.page = label
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
if not st.secrets.get("hf_token", ""):
    st.markdown(
        '<div class="err-strip">⚠️ <b>HF token missing.</b> '
        'Add <code>hf_token = "hf_..."</code> to <code>.streamlit/secrets.toml</code>.</div>',
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
    for icon, name, detail, ts in [
        ("🖼️", "landscape.jpg",  "Scene Description · 3 messages", "2 hours ago"),
        ("🖼️", "screenshot.png", "Text Extraction · 1 message",   "Yesterday"),
        ("🖼️", "photo.jpg",      "Object Detection · 5 messages", "3 days ago"),
    ]:
        st.markdown(f"""
        <div class="hist-item">
            <div style="font-size:1.4rem;">{icon}</div>
            <div style="flex:1;">
                <div style="font-weight:600;font-size:.9rem;color:#E2E8F0;">{name}</div>
                <div style="font-size:.8rem;color:#64748B;">{detail}</div>
            </div>
            <div style="font-size:.78rem;color:#475569;">{ts}</div>
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
    for label, value, sub in [
        ("🤖 AI Model",        "deepseek-ai/DeepSeek-V4-Flash-Vision-Exp", "Active vision model"),
        ("🔑 API Token",       "Configured via secrets.toml",              "Stored securely"),
        ("🎨 Theme",           "Dark Mode",                                "Default appearance"),
        ("📁 Max Upload",      "10 MB",                                    "Set in config.toml"),
        ("🌐 Language",        "English",                                  "Interface language"),
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
        <div class="hero-sub">Upload an image and let VisionAI analyze, describe, and answer questions about it.</div>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("drop", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded:
        ok, err, img = validate_image(uploaded)
        if ok:
            st.session_state.img_hash  = hash(uploaded.getvalue())
            st.session_state.img_bytes = uploaded.getvalue()
            st.session_state.img_name  = uploaded.name
            st.session_state.img_size  = len(uploaded.getvalue())
            st.session_state.analysis  = None
            st.session_state.messages  = []
            st.rerun()
        else:
            st.error(f"⚠️ {err}")
    st.stop()

# ── State 2+: Image is in session ─────────────────────────────────────
img_pil = Image.open(io.BytesIO(st.session_state.img_bytes))

# "New Image" button top-right
_, col_tr = st.columns([5, 1])
with col_tr:
    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
    if st.button("↩ New Image"):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Centered image display — use st.image directly (no wrapping divs)
_, col_img, _ = st.columns([1, 5, 1])
with col_img:
    st.image(img_pil, use_container_width=True)
    size_kb = st.session_state.img_size / 1024
    st.markdown(
        f'<p style="text-align:center;color:#475569;font-size:.82rem;margin-top:.3rem;margin-bottom:1.5rem;">'
        f'{st.session_state.img_name} · {size_kb:.1f} KB · {img_pil.width}×{img_pil.height}</p>',
        unsafe_allow_html=True,
    )

# ── State 2: Awaiting analysis ────────────────────────────────────────
if st.session_state.analysis is None:
    _, col_btn, _ = st.columns([2, 2, 2])
    with col_btn:
        if st.button("✨  Analyze Image"):
            with st.spinner("Analyzing image…"):
                try:
                    b64 = to_b64(img_pil)
                    resp = hf_chat([{
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                            {"type": "text", "text": """\
You are VisionAI, an AI image understanding assistant.

Analyze the uploaded image carefully and describe only what is visibly present. Do not guess, assume, or invent details.

Follow this exact output format:

## ✨ AI Description
Write 1–2 natural paragraphs describing the image.

Include, when clearly visible:
1. Overall scene — briefly explain what the image shows.
2. Main subjects — identify the important people, animals, objects, or elements.
3. Actions — describe what the subjects are doing.
4. Environment — describe the location, background, and surroundings.
5. Important details — mention notable colors, clothing, objects, positions, lighting, or other visible details.
6. Visible text — accurately mention readable text appearing in the image.

## 🔍 Detected Details
- **Subjects:** List the main subjects.
- **Action:** Describe what they are doing.
- **Location:** Describe the apparent setting.
- **Environment:** Describe important surroundings.
- **Mood:** Describe the visual atmosphere only if it can reasonably be inferred from the image.

Rules:
- Describe only information supported by the image.
- Never invent names, locations, events, emotions, or objects.
- If something is uncertain, use phrases such as "appears to be" or "possibly."
- Do not repeat the same information.
- Keep the description clear, natural, and informative.
- Do not mention that you are an AI.
- Do not describe your analysis process.
- If text is present but unreadable, say "Unreadable text is visible.\""""}
                        ]
                    }])
                    st.session_state.analysis = resp
                    st.rerun()
                except Exception as e:
                    st.error(f"API Error: {e}")
    st.stop()

# ── State 3+: Analysis ready ──────────────────────────────────────────
_, col_main, _ = st.columns([1, 5, 1])
with col_main:
    desc_text, detail_rows = parse_analysis(st.session_state.analysis)

    # Description card
    st.markdown("""
    <div class="glass-panel">
        <div class="panel-heading">
            <span style="font-size:1.1rem;">✨</span>
            <span class="panel-heading-text">AI Description</span>
        </div>
        <div class="panel-divider"></div>
    </div>""", unsafe_allow_html=True)
    # Render description text via st.markdown so markdown formatting works
    st.markdown(desc_text)

    # Detected Details card — fully inline HTML (values are from AI, HTML-safe enough)
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
        # Build full conversation history for the API
        history = [
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": "Here is the image for context."},
            ]},
            {"role": "assistant", "content": st.session_state.analysis},
        ]
        for m in st.session_state.messages:
            history.append({"role": m["role"], "content": m["text"]})

        try:
            ai_resp = hf_chat(history)
            st.session_state.messages.append({"role": "assistant", "text": ai_resp})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "text": f"❌ {e}"})
    st.rerun()
