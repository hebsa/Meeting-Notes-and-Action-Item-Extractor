# Meeting-Notes-and-Action-Item-Extractor
Create an app to convert meeting audio into structured notes and task lists using Whisper and OpenAI APIs.

# 🎙️ Meeting Notes & Task Extractor (Offline)

## 📝 Overview
The **Meeting Notes & Task Extractor** is a Streamlit-based application that allows users to:
1. Upload an audio file of a meeting.
2. Transcribe the meeting using **Whisper** (runs locally, no API key needed).
3. Extract actionable tasks using a local HuggingFace model (**Flan-T5-base**).

This project runs fully **offline** — no OpenAI API key required.

---

## ⚡ Features
- 🎧 Audio transcription with Whisper (local model).
- ✅ Automatic task extraction from transcripts using HuggingFace transformers.
- 🖥️ Streamlit web-based interface.
- 🔒 100% offline, secure, and free to run locally.

---

## 🛠️ Tech Stack
- **Python 3.9+**
- [Streamlit](https://streamlit.io/) → UI framework.
- [Whisper](https://github.com/openai/whisper) → Speech-to-text transcription.
- [Transformers (Hugging Face)](https://huggingface.co/transformers/) → Task extraction (Flan-T5-base model).
- **Torch** → Required for model inference.

---

## 📦 Installation

1. Clone or download this project folder.

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the environment:
- **Windows (PowerShell):**
```bash
.
env\Scripts\Activate.ps1
```
- **Windows (cmd):**
```bash
.
env\Scripts ctivate.bat
```
- **Mac/Linux:**
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```
Or install manually:
```bash
pip install streamlit openai-whisper transformers torch
```

5. Install **FFmpeg** (required by Whisper):
   - Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
   - Add the `bin` folder to your **PATH**.

---

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run meeting_notes_app.py
```

Steps:
1. Upload your meeting audio file (`.mp3`, `.wav`, `.m4a`).
2. Click **Process**.
3. View the **Transcript** and **Extracted Tasks**.

---

## 📂 Project Structure
```
Meeting Notes Extractor/
│── meeting_notes_app.py    # Main Streamlit app
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
```

---

## 📌 Example Output

**Transcript**
```
Good afternoon, everyone. Let's begin with the updates...
```

**Extracted Tasks**
```
Task 1: Review the shared evidence
Task 2: Update the project tracker
Task 3: Ensure changes are reflected in documentation
Task 4: Close the testing phase once validated
```

---

## 🚀 Future Improvements
- Improve task extraction with fine-tuned local models.
- Add speaker diarization (who said what).
- Export tasks directly to Excel or Notion.

---

## 👨‍💻 Author
Developed as part of **SEQATO LLM Awareness and Portfolio Development Program**.
