---
title: VisionAI
emoji: 👁️
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: "1.44.1"
app_file: app.py
pinned: false
license: mit
---

# 👁️ VisionAI — AI-Powered Image Understanding Studio

**VisionAI** is a sleek, dark-themed web application that uses **multiple state-of-the-art vision-language models** via the OpenRouter API (100% free) to analyze uploaded images with **6 specialized analysis modes** and answer follow-up questions in a real-time chat interface.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![OpenRouter](https://img.shields.io/badge/OpenRouter-Free_API-635BFF)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Image Upload** | Drag-and-drop or browse for JPG, PNG, WEBP, BMP, TIFF, GIF images |
| 🧩 **6 Analysis Modes** | Describe, Extract Text (OCR), Detect Objects, Color & Style, Code from Image, Creative Writing |
| 💬 **Visual Q&A Chat** | Ask follow-up questions about the image in a mode-aware real-time chat |
| 🔄 **Auto Model Shifting** | Automatically rotates across 6+ vision models per request for best coverage |
| 🛡️ **Automatic Fallback** | If a model fails or is rate-limited, shifts to the next one, with `openrouter/auto` as last resort |
| 🎨 **Premium Dark UI** | Glassmorphism panels, gradient hero, styled chat bubbles, Inter + JetBrains Mono fonts |
| 📋 **Mode-Specific Output** | Each mode renders results in a specialized format (tables, code blocks, color swatches, prose) |
| 🧭 **Multi-page Navigation** | Sidebar with Workspace, History, Saved, and Settings pages |
| 🕒 **Session History** | Real history tracking of all analyses performed during a session |
| 🚀 **HF Spaces Ready** | Deploys directly to Hugging Face Spaces with a single secret |

---

## 🧩 Analysis Modes

VisionAI provides **6 specialized analysis modes**, each with a carefully crafted prompt and tailored output format:

| Mode | Icon | Description |
|------|------|-------------|
| **Describe** | ✨ | Full scene description with detected details (subjects, action, location, mood) |
| **Extract Text** | 📝 | OCR — reads ALL text from images: signs, documents, receipts, handwriting |
| **Detect Objects** | 🎯 | Lists every distinct object with count, position, size, and confidence level |
| **Color & Style** | 🎨 | Extracts dominant colors (hex codes), art style, composition, and lighting analysis |
| **Code from Image** | 💻 | Converts UI screenshots into clean, semantic HTML/CSS code |
| **Creative Writing** | ✍️ | Generates original stories, poems, or vignettes inspired by the image |

After analyzing with one mode, you can instantly **re-analyze with any other mode** without re-uploading the image.

---

## 🤖 Vision Models (Auto-Shifting)

The app automatically rotates between **6 powerful free vision models** in round-robin order. If any model fails, it silently falls back to the next one:

| # | Model | Strengths |
|---|---|---|
| 1 | **Google Gemma 4 31B IT** | Best quality, vision + video support |
| 2 | **Google Gemma 4 26B A4B IT** | Fast inference, vision + video support |
| 3 | **InclusionAI Ling 3.0 Flash VL** | Vision-Language specialist |
| 4 | **NVIDIA Nemotron 3 Nano Omni** | Strong reasoning capabilities |
| 5 | **Dots Studio Dots 3 Note** | Versatile text and image understanding |
| 6 | **Nex AGI Nex N2.5 Mini** | Compact but capable |
| 🔄 | **OpenRouter Auto** | Last-resort auto-router fallback |

> No model selection is needed — the app handles it automatically every request. The model used is shown as a badge after each analysis.

---

## 🚀 Quick Start — Run Locally

### Prerequisites

- Python 3.9 or higher
- A free [OpenRouter account](https://openrouter.ai) with an API key (`sk-or-v1-...`)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/pavAN2006/VisionAI.git
cd VisionAI

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenRouter API key
# Create .streamlit/secrets.toml with:
# openrouter_api_key = "sk-or-v1-YOUR_KEY_HERE"

# 5. Run the app
python -m streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## 🔑 API Key Setup

This app uses the **OpenRouter API** with 100% free vision models — no GPU or paid subscription required.

1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Create a free API key (no credit card needed)
3. Create the file `.streamlit/secrets.toml` in the project root:

```toml
openrouter_api_key = "sk-or-v1-YOUR_KEY_HERE"
```

> ⚠️ `.streamlit/secrets.toml` is listed in `.gitignore` and will never be committed.

### Rate Limits (Free Tier)

| Limit | Value |
|-------|-------|
| Requests per minute | 20 |
| Requests per day (free account) | 50 |
| Requests per day ($10 one-time credit purchase) | 1,000 |
| Cost per token | $0 (always free for `:free` models) |

---

## ☁️ Deploy to Hugging Face Spaces

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select **Streamlit** as the SDK
3. Push your code to the Space repository
4. In Space **Settings → Secrets**, add:
   - `openrouter_api_key` = `sk-or-v1-YOUR_KEY_HERE`
5. The Space will build and deploy automatically

---

## 📁 Project Structure

```
VisionAI/
├── app.py                  # Main Streamlit application (6 analysis modes)
├── requirements.txt        # Python dependencies
├── README.md               # Documentation + HF Spaces metadata
├── .gitignore              # Git ignore rules (secrets excluded)
└── .streamlit/
    ├── config.toml         # Streamlit theme & server config
    └── secrets.toml        # OpenRouter API key (local only, not committed)
```

---

## 🛠️ How It Works

1. **Upload** — The user uploads an image via the Streamlit file uploader (JPG, PNG, WEBP, BMP, TIFF, GIF).
2. **Validate** — The image is validated for format and integrity.
3. **Choose Mode** — The user selects one of 6 analysis modes from a card grid.
4. **Encode** — The image is resized to max 512px and base64-encoded for the API.
5. **Analyze** — A mode-specific prompt is sent to OpenRouter with the image.
6. **Render** — Results are rendered in mode-specific formats (glass panels, code blocks, tables, prose).
7. **Re-analyze** — Users can switch to a different mode on the same image instantly.
8. **Chat** — Follow-up questions are mode-aware, referencing the active analysis context.

### Auto Model-Shifting Logic

```
Request → Try Model[idx % 6]
  ✅ Success → return response, advance idx
  ❌ Failure → advance idx, try next model
  ❌×6 All fail → try openrouter/auto (last resort)
  ❌×7 Auto fails → raise error to user
```

---

## 💰 Is It Really Free?

**Yes.** Here's the breakdown:

| Component | Cost | Forever? |
|-----------|------|----------|
| Streamlit | Free | ✅ Open source |
| Python / Pillow / Requests | Free | ✅ Open source |
| OpenRouter `:free` models | $0 per token | ✅ As long as free models exist |
| OpenRouter API key | Free to create | ✅ No credit card needed |
| Hugging Face Spaces (deploy) | Free tier | ✅ 2 free CPU spaces |

> You will **never be charged** unless you manually add payment and switch to paid models. The `:free` suffix guarantees $0 cost.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 Acknowledgements

- [Google](https://ai.google/) — Gemma 4 vision models
- [InclusionAI](https://github.com/inclusionai) — Ling 3.0 Flash VL model
- [NVIDIA](https://www.nvidia.com/) — Nemotron 3 Nano Omni model
- [Dots Studio](https://dots.studio/) — Dots 3 Note model
- [Nex AGI](https://nex-agi.com/) — Nex N2.5 Mini model
- [OpenRouter](https://openrouter.ai) — Unified API with free model access
- [Streamlit](https://streamlit.io) — Web application framework
