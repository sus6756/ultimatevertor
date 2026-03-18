import streamlit as st
import tempfile
import pandas as pd
import subprocess
from pdf2docx import Converter
from docx import Document
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="Ultimate Converter", layout="wide")

# ================= UI STYLE =================
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
}
.sub-text {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🔥 Ultimate Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Convert files, video, audio — everything 🚀</div>', unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Documents",
    "🖼️ Images",
    "📊 Data",
    "🎥 Video",
    "🎵 Audio"
])

# ================= DOCUMENTS =================
with tab1:
    st.subheader("📄 Document Converter")

    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "txt"])

    option = st.selectbox("Choose Conversion", [
        "PDF to DOCX",
        "DOCX to PDF",
        "TXT to DOCX",
        "DOCX to TXT"
    ])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("🚀 Convert Document"):
            with st.spinner("Processing..."):
                try:
                    if option == "PDF to DOCX":
                        output = file_path + ".docx"
                        cv = Converter(file_path)
                        cv.convert(output)
                        cv.close()

                    elif option == "DOCX to PDF":
                        subprocess.run([
                            "soffice",
                            "--headless",
                            "--convert-to",
                            "pdf",
                            file_path,
                            "--outdir",
                            "."
                        ], check=True)
                        output = file_path.replace(".docx", ".pdf")

                    elif option == "TXT to DOCX":
                        doc = Document()
                        with open(file_path, "r") as f:
                            doc.add_paragraph(f.read())
                        output = file_path + ".docx"
                        doc.save(output)

                    elif option == "DOCX to TXT":
                        doc = Document(file_path)
                        text = "\n".join([p.text for p in doc.paragraphs])
                        st.download_button("Download TXT", text)
                        st.success("Done ✅")
                        st.stop()

                    with open(output, "rb") as f:
                        st.download_button("📥 Download", f)

                    st.success("Done ✅")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================= IMAGES =================
with tab2:
    st.subheader("🖼️ Image → PDF")

    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        if st.button("🚀 Convert Image"):
            with st.spinner("Processing..."):
                image = Image.open(uploaded_file)
                output = "output.pdf"
                image.convert("RGB").save(output)

                with open(output, "rb") as f:
                    st.download_button("📥 Download PDF", f)

# ================= DATA =================
with tab3:
    st.subheader("📊 CSV ↔ Excel")

    uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

    option = st.selectbox("Choose Conversion", ["CSV to Excel", "Excel to CSV"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("🚀 Convert Data"):
            with st.spinner("Processing..."):
                if option == "CSV to Excel":
                    df = pd.read_csv(file_path)
                    output = file_path + ".xlsx"
                    df.to_excel(output, index=False)

                else:
                    df = pd.read_excel(file_path)
                    output = file_path + ".csv"
                    df.to_csv(output, index=False)

                with open(output, "rb") as f:
                    st.download_button("📥 Download", f)

# ================= VIDEO =================
with tab4:
    st.subheader("🎥 Video Converter")

    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    format_choice = st.selectbox("Convert to", ["mp4", "avi", "mov"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("🚀 Convert Video"):
            with st.spinner("Processing..."):
                clip = VideoFileClip(file_path)
                output = file_path + f".{format_choice}"
                clip.write_videofile(output)

                with open(output, "rb") as f:
                    st.download_button("📥 Download Video", f)

# ================= AUDIO =================
with tab5:
    st.subheader("🎵 Audio Converter")

    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])

    format_choice = st.selectbox("Convert to", ["mp3", "wav"])

    if uploaded_file:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded_file.read())
        file_path = temp.name

        if st.button("🚀 Convert Audio"):
            with st.spinner("Processing..."):
                audio = AudioFileClip(file_path)
                output = file_path + f".{format_choice}"
                audio.write_audiofile(output)

                with open(output, "rb") as f:
                    st.download_button("📥 Download Audio", f)
