# === FRONTEND (app.py) ===

import streamlit as st
import tempfile
import os
from backend import generate_quiz_from_pdf

st.set_page_config(page_title="RAG Quiz Generator", layout="wide")
st.title("📘 Quiz Generator using RAG + LangChain")

uploaded_file = st.file_uploader("Upload a textbook PDF", type="pdf")

if uploaded_file:
    st.success("PDF uploaded. Generating quiz...")

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("Processing with LangChain + Gemini..."):
        try:
            quiz_output = generate_quiz_from_pdf(tmp_path)
            st.success("Quiz generated successfully!")
        except Exception as e:
            st.error(f"Error generating quiz: {e}")
            os.remove(tmp_path)
            st.stop()

    # Show quiz output
    st.subheader("📝 Generated Quiz")
    st.text_area("Formatted Quiz", quiz_output, height=500)

    # Optionally allow download
    st.download_button(
        label="📥 Download Quiz as Text",
        data=quiz_output,
        file_name="generated_quiz.txt",
        mime="text/plain"
    )

    os.remove(tmp_path)
