import os
import subprocess
import whisper
import streamlit as st
from datetime import datetime
from tempfile import NamedTemporaryFile
import re

# ========== TASK/NOTE EXTRACTOR ==========
def generate_meeting_notes_and_tasks(transcript_text):
    sentences = re.split(r'(?<=[.!?]) +', transcript_text)

    task_keywords = [
        "please", "ensure", "share", "fix", "update", "send", "complete",
        "check", "mention", "pending", "approve", "notify", "assign"
    ]

    tasks = []
    notes = []

    for sentence in sentences:
        stripped = sentence.strip()
        if not stripped:
            continue
        if any(kw in stripped.lower() for kw in task_keywords):
            tasks.append(f"✅ {stripped}")
        elif len(stripped.split()) > 4:
            notes.append(f"🧠 {stripped}")

    notes_text = "\n".join(notes) if notes else "No notes found."
    tasks_text = "\n".join(tasks) if tasks else "No action items found."

    return notes_text.strip(), tasks_text.strip()

# ========== TRANSCRIPTION ==========
@st.cache_resource(show_spinner=False)
def load_model():
    return whisper.load_model("base")

@st.cache_data(show_spinner=False)
def transcribe_audio(file_path):
    model = load_model()
    result = model.transcribe(file_path)
    return result["text"]

# ========== AUDIO HANDLING ==========
def save_and_prepare_audio(uploaded_file):
    filename = uploaded_file.name
    base_name, ext = os.path.splitext(filename)
    temp_input_path = f"temp_input{ext.lower()}"

    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.read())

    if ext.lower() == ".mkv":
        st.info("🎬 Converting .mkv to .mp3...")
        converted_path = "temp_converted.mp3"
        subprocess.run([
            "ffmpeg", "-i", temp_input_path,
            "-vn", "-acodec", "libmp3lame", "-y", converted_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(temp_input_path)
        return converted_path

    return temp_input_path

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="🎙️ Meeting Notes & Task Extractor", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #4a7ebB;'>🎙️ Meeting Notes & Task Extractor</h1>
    <p style='text-align: center;'>Upload your meeting audio file to generate a transcript, summary, and task list automatically!</p>
    <hr>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload an audio file", type=["mp3", "wav", "m4a", "mkv"])

if uploaded_file:
    audio_path = save_and_prepare_audio(uploaded_file)

    with st.spinner("Transcribing audio... ⏳"):
        transcript = transcribe_audio(audio_path)

    notes, tasks = generate_meeting_notes_and_tasks(transcript)

    st.success("✅ Transcription & summary complete!")

    st.subheader("📄 Transcript")
    st.text_area("Transcript", transcript, height=200)

    st.subheader("🧠 Meeting Notes")
    st.code(notes, language='markdown')

    st.subheader("✅ Action Items / Task List")
    st.code(tasks, language='markdown')

    # ========== DOWNLOAD ==========
    summary_content = (
        f"Meeting Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"\n---\n\n"
        f"**Transcript:**\n{transcript}\n\n"
        f"**Meeting Notes:**\n{notes}\n\n"
        f"**Action Items:**\n{tasks}"
    )

    with NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
        temp_file.write(summary_content)
        summary_path = temp_file.name

    with open(summary_path, "rb") as f:
        st.download_button(
            label="📥 Download Notes as .txt",
            data=f,
            file_name="meeting_summary.txt",
            mime="text/plain"
        )

    # 🔁 Upload Another File
    st.markdown("---")
    if st.button("🔁 Upload Another Meeting File"):
        st.rerun()

    # Clean up temp audio file
    if os.path.exists(audio_path) and audio_path.startswith("temp_"):
        os.remove(audio_path)
