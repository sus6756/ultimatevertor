import streamlit as st
import tempfile
import pandas as pd
from pdf2docx import Converter
from docx2pdf import convert
from docx import Document
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="Ultimate Converter", layout="centered")

st.title("🔥 ULTIMATE CONVERTER")
st.write("Convert files, video, audio, everything 😎")

# =========================
# CATEGORY SELECT
# =========================
category = st.selectbox("Choose Category", [
    "PDF ↔ DOCX",
    "TXT ↔ DOCX",
    "Image → PDF",
    "CSV ↔ Excel",
    "Video Converter",
    "Audio Converter",
    "Video → Audio",
])

uploaded_file = st.file_uploader("Upload file")

# =========================
# PDF ↔ DOCX
# =========================
if category == "PDF ↔ DOCX":
    option = st.selectbox("Conversion", ["PDF to DOCX", "DOCX to PDF"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Convert"):
            if option == "PDF to DOCX":
                output = file_path + ".docx"
                cv = Converter(file_path)
                cv.convert(output)
                cv.close()

                with open(output, "rb") as f:
                    st.download_button("Download DOCX", f)

            elif option == "DOCX to PDF":
                output = file_path + ".pdf"
                convert(file_path, output)

                with open(output, "rb") as f:
                    st.download_button("Download PDF", f)

# =========================
# TXT ↔ DOCX
# =========================
elif category == "TXT ↔ DOCX":
    option = st.selectbox("Conversion", ["TXT to DOCX", "DOCX to TXT"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Convert"):
            if option == "TXT to DOCX":
                doc = Document()
                with open(file_path, "r") as f:
                    doc.add_paragraph(f.read())

                output = file_path + ".docx"
                doc.save(output)

                with open(output, "rb") as f:
                    st.download_button("Download DOCX", f)

            elif option == "DOCX to TXT":
                doc = Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
                st.download_button("Download TXT", text)

# =========================
# IMAGE → PDF
# =========================
elif category == "Image → PDF":
    if uploaded_file:
        image = Image.open(uploaded_file)

        if st.button("Convert"):
            output = "output.pdf"
            image.convert("RGB").save(output)

            with open(output, "rb") as f:
                st.download_button("Download PDF", f)

# =========================
# CSV ↔ EXCEL
# =========================
elif category == "CSV ↔ Excel":
    option = st.selectbox("Conversion", ["CSV to Excel", "Excel to CSV"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Convert"):
            if option == "CSV to Excel":
                df = pd.read_csv(file_path)
                output = file_path + ".xlsx"
                df.to_excel(output, index=False)

                with open(output, "rb") as f:
                    st.download_button("Download Excel", f)

            elif option == "Excel to CSV":
                df = pd.read_excel(file_path)
                output = file_path + ".csv"
                df.to_csv(output, index=False)

                with open(output, "rb") as f:
                    st.download_button("Download CSV", f)

# =========================
# VIDEO CONVERTER
# =========================
elif category == "Video Converter":
    format_choice = st.selectbox("Convert to", ["mp4", "avi", "mov"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Convert Video"):
            clip = VideoFileClip(file_path)
            output = file_path + f".{format_choice}"
            clip.write_videofile(output)

            with open(output, "rb") as f:
                st.download_button("Download Video", f)

# =========================
# AUDIO CONVERTER
# =========================
elif category == "Audio Converter":
    format_choice = st.selectbox("Convert to", ["mp3", "wav"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Convert Audio"):
            audio = AudioFileClip(file_path)
            output = file_path + f".{format_choice}"
            audio.write_audiofile(output)

            with open(output, "rb") as f:
                st.download_button("Download Audio", f)

# =========================
# VIDEO → AUDIO
# =========================
elif category == "Video → Audio":
    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("Extract Audio"):
            clip = VideoFileClip(file_path)
            output = file_path + ".mp3"
            clip.audio.write_audiofile(output)

            with open(output, "rb") as f:
                st.download_button("Download MP3", f)
