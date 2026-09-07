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

**VisionAI** is a sleek, dark-themed web application that uses **multiple state-of-the-art vision-language models** via the Hugging Face Inference API to analyze uploaded images, generate rich AI descriptions, and answer follow-up questions in a real-time chat interface.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-Inference_API-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Image Upload** | Drag-and-drop or browse for JPG or PNG images |
| 🤖 **AI Image Analysis** | One-click deep image analysis with structured output |
| 💬 **Visual Q&A Chat** | Ask follow-up questions about the image in a real-time chat |
| 🔄 **Auto Model Shifting** | Automatically rotates across 3 vision models per request for best coverage |
| 🛡️ **Automatic Fallback** | If a model fails or is rate-limited, instantly shifts to the next one |
| ♻️ **Connection Pooling** | Cached `InferenceClient` prevents socket leaks across multiple sessions |
| 🎨 **Premium Dark UI** | Glassmorphism panels, gradient hero, styled chat bubbles, Inter font |
| 📋 **Structured Output** | AI Description card + Detected Details key-value panel |
| 🧭 **Multi-page Navigation** | Sidebar with Workspace, History, Saved, and Settings pages |
| 🚀 **HF Spaces Ready** | Deploys directly to Hugging Face Spaces with a single secret |

---

## 🤖 Vision Models (Auto-Shifting)

The app automatically rotates between three powerful vision models in round-robin order. If any model fails, it silently falls back to the next one:

| # | Model | Strengths |
|---|---|---|
| 1 | **DeepSeek-V4-Flash-Vision-Exp** | Fast inference, strong general vision understanding |
| 2 | **Llama 3.2 11B Vision Instruct** | Excellent instruction following and reasoning |
| 3 | **Qwen2 VL 7B Instruct** | Strong multilingual and detailed visual analysis |

> No model selection is needed — the app handles it automatically every request.

---

## 🚀 Quick Start — Run Locally

### Prerequisites

- Python 3.9 or higher
- A free [Hugging Face account](https://huggingface.co) with an API token (`hf_...`)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/VisionAI
cd VisionAI

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your HuggingFace token
# Create .streamlit/secrets.toml with:
# hf_token = "hf_YOUR_TOKEN_HERE"

# 5. Run the app
python -m streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

---

## 🔑 API Token Setup

This app uses the **Hugging Face Inference API** — no local GPU required.

1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a token with **Read** permissions (free)
3. Create the file `.streamlit/secrets.toml` in the project root:

```toml
hf_token = "hf_YOUR_TOKEN_HERE"
```

> ⚠️ `.streamlit/secrets.toml` is listed in `.gitignore` and will never be committed.

---

## ☁️ Deploy to Hugging Face Spaces

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select **Streamlit** as the SDK
3. Push your code to the Space repository
4. In Space **Settings → Secrets**, add:
   - `hf_token` = `hf_YOUR_TOKEN_HERE`
5. The Space will build and deploy automatically

---

## 📁 Project Structure

```
VisionAI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Documentation + HF Spaces metadata
├── .gitignore              # Git ignore rules (secrets excluded)
└── .streamlit/
    ├── config.toml         # Streamlit theme & server config
    └── secrets.toml        # HF API token (local only, not committed)
```

---

## 🛠️ How It Works

1. **Upload** — The user uploads a JPG/PNG image via the Streamlit file uploader.
2. **Validate** — The image is validated for format and integrity.
3. **Encode** — The image is resized to max 1024px and base64-encoded for the API.
4. **Analyze** — A structured prompt is sent to the Inference API with the image, requesting a detailed AI description and a key-value detected details block.
5. **Parse** — The response is parsed into a description paragraph and a structured detail table.
6. **Display** — Results are rendered in glass-panel cards with the AI description and detected details.
7. **Chat** — The user can ask follow-up questions; each message re-sends the image with the full conversation history flattened into a single context-aware prompt.

### Auto Model-Shifting Logic

```
Request → Try Model[idx % 3]
  ✅ Success → return response, advance idx
  ❌ Failure → advance idx, try next model
  ❌❌❌ All 3 fail → raise error to user
```

### Connection Pooling

The `InferenceClient` is cached via `@st.cache_resource`, keyed by the API token. This means **one persistent connection is reused** across all reruns and image uploads, preventing network socket exhaustion.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 Acknowledgements

- [DeepSeek](https://www.deepseek.com/) — DeepSeek-V4-Flash-Vision model
- [Meta AI](https://ai.meta.com/) — Llama 3.2 Vision model
- [Qwen Team (Alibaba Cloud)](https://github.com/QwenLM) — Qwen2-VL model
- [Hugging Face](https://huggingface.co) — Inference API & Spaces platform
- [Streamlit](https://streamlit.io) — Web application framework

