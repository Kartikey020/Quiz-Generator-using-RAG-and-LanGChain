# 📚 Quiz Generator using RAG and LangChain

This project is an intelligent **educational quiz generator** that uses **RAG (Retrieval-Augmented Generation)** and **LangChain** to convert any educational PDF (textbooks, class notes, etc.) into structured self-assessment quizzes including:
- Multiple Choice Questions (MCQs)
- Fill-in-the-Blanks
- True/False Questions

It offers both a backend (Python + LangChain) and a frontend (Streamlit) for easy interaction and download.

---

## 🚀 Features

- 🔍 **PDF Input Support** – Upload any textbook or notes.
- 🧠 **RAG Pipeline** – Uses FAISS and HuggingFace embeddings to retrieve context.
- 🤖 **Question Generation** – Uses `google/flan-t5-large` to generate questions.
- 🧾 **Formatted Quizzes** – Structured quiz formatting using Gemini Pro.
- 📥 **PDF Download** – Export quiz as a styled PDF.
- 🖥️ **Streamlit Frontend** – Easy UI for uploading and generating quizzes.

---

## 🧠 Tech Stack

### 🖥️ Frontend
- Streamlit

### ⚙️ Backend
- Python
- LangChain
- FAISS Vector Store
- HuggingFace Transformers
- Google Generative AI (Gemini Pro)
- PyMuPDF (`fitz`)
- FPDF

---

## 🛠️ How It Works

1. **User uploads a PDF** (e.g., biology textbook).
2. **Text is extracted and chunked** using `CharacterTextSplitter`.
3. **Chunks are embedded** using HuggingFace Embeddings and stored in FAISS.
4. **`google/flan-t5-large`** generates quiz questions from each chunk.
5. **Gemini Pro** formats questions into a readable quiz.
6. **PDF is created** and can be downloaded by the user.

---

## 📦 Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/quiz-generator.git
   cd quiz-generator
2.Install dependencies:
   ```bash
  pip install -r requirements.txt
```
3.Run streamlit frontend:
```
  streamlit run app.py
```
4.Upload any textbook or notes PDF and generate quizzes!


🔒 Note
This project does not store any user data.

Ensure large model files or venv/ are not tracked by Git to avoid push errors.
