---
title: VisionAI
emoji: 🔍
colorFrom: indigo
colorTo: green
sdk: streamlit
sdk_version: "1.44.1"
app_file: app.py
pinned: false
license: mit
---

# 🔍 VisionAI — AI-Powered Image Description Generator

**VisionAI** is a web application that uses the **Qwen2.5-VL-3B-Instruct** vision-language model to generate natural-language descriptions of uploaded images. Upload any photo and get an instant, AI-generated description — no API keys, no cost, 100% open-source.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-Spaces-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Image Upload** | Drag-and-drop or browse for JPG, JPEG, or PNG images |
| 📝 **Short Description** | Concise one-line caption |
| 📖 **Detailed Description** | Rich paragraph with 3-5 sentences covering subject, setting, colors, lighting, mood |
| 🔬 **Pixel-Level Analysis** | Exhaustive single-pass analysis covering scene composition, subjects, color palette, lighting, textures, spatial layout, atmosphere, and fine details |
| ⚡ **Auto Hardware Detection** | Automatically uses GPU (CUDA/MPS) if available, otherwise CPU |
| 🧠 **Model Caching** | Model loads once and stays in memory for fast subsequent requests |
| 🎨 **Modern UI** | Dark theme with gradient accents and smooth interactions |
| 🛡️ **Error Handling** | Graceful handling of invalid files, corrupt images, and model errors |
| 🚀 **HF Spaces Ready** | Deployable directly to Hugging Face Spaces |

---

## 🧠 Model

**[Qwen/Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct)**

- **Architecture**: Qwen2.5-VL (Vision-Language) with instruction tuning
- **Parameters**: ~3B
- **License**: Apache-2.0 (open-source, free for commercial use)
- **Capabilities**: Image understanding, visual question answering, detailed image description, instruction following
- **Hardware**: Runs on CPU (~12 GB RAM) and GPU (~6 GB VRAM in float16)

---

## 🚀 Quick Start — Run Locally

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- ~12 GB free RAM (CPU) or ~6 GB VRAM (GPU)
- ~6 GB free disk space (for model download on first run)

### Steps

```bash
# 1. Clone the repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/VisionAI
cd VisionAI

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

> **Note:** The first run will download the Qwen2.5-VL-3B model (~6 GB). Subsequent runs use the cached model and start faster.

---

## ☁️ Deploy to Hugging Face Spaces

### Option A — Via the Hugging Face Web UI

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose a name (e.g., `VisionAI`)
3. Select **Streamlit** as the SDK
4. Upload all project files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.streamlit/config.toml`
5. The Space will build and deploy automatically

### Option B — Via Git

```bash
# 1. Create a new Space on Hugging Face (SDK: Streamlit)

# 2. Clone the Space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/VisionAI
cd VisionAI

# 3. Copy your project files into the repo

# 4. Push
git add .
git commit -m "Initial deploy of VisionAI"
git push
```

> **Tip:** Hugging Face Spaces provides a free CPU tier. For faster inference, upgrade to a GPU runtime in Space settings.

---

## 📁 Project Structure

```
VisionAI/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Documentation + HF Spaces metadata
├── .gitignore              # Git ignore rules
└── .streamlit/
    └── config.toml         # Streamlit theme & server config
```

---

## 🛠️ Technical Details

### How It Works

1. **Upload** — The user uploads a JPG/JPEG/PNG image via the Streamlit file uploader.
2. **Validate** — The image is validated (format, integrity, non-empty).
3. **Process** — The image is converted to RGB and processed by the Qwen2.5-VL processor.
4. **Generate** — The model receives a chat-style message with the image and a mode-specific instruction prompt:
   - *Short*: "Describe this image in one concise sentence."
   - *Detailed*: Multi-aspect prompt requesting 3-5 sentences.
   - *Pixel-Level*: Exhaustive prompt requesting analysis of 10 visual dimensions.
5. **Display** — The generated description is shown in a styled result card.

### Hardware Detection

| Priority | Device | When Used |
|---|---|---|
| 1 | CUDA GPU | NVIDIA GPU with CUDA drivers installed |
| 2 | MPS | Apple Silicon Mac (M1/M2/M3) |
| 3 | CPU | Fallback — works everywhere, slower |

### Performance

| Device | Short | Detailed | Pixel-Level |
|---|---|---|---|
| NVIDIA T4 GPU | ~3-5s | ~8-12s | ~15-30s |
| CPU (Intel i7, 16 GB) | ~30-60s | ~1-2 min | ~2-5 min |

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

The Qwen2.5-VL-3B-Instruct model is licensed under the [Apache-2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

---

## 🙏 Acknowledgements

- [Qwen Team (Alibaba Cloud)](https://github.com/QwenLM/Qwen2.5-VL) — Qwen2.5-VL model
- [Hugging Face](https://huggingface.co) — Model hosting and Spaces platform
- [Streamlit](https://streamlit.io) — Web application framework
