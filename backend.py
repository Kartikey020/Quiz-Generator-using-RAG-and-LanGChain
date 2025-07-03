# === BACKEND (backend.py) ===

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import google.generativeai as genai

# Extract text from PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# Chunk the text
text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=100)

# Embedding and vector store setup
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vectorstore(text):
    chunks = text_splitter.split_text(text)
    vectorstore = FAISS.from_texts(chunks, embedding_model)
    return vectorstore, chunks

# QA generator model
model_id = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

# Generate QA pairs
def generate_questions(chunks):
    mcqs, blanks, tfs = [], [], []
    for i, chunk in enumerate(chunks[:20]):
        prompt_mcq = f"Generate 2 MCQ with 4 options and the correct answer:\n{chunk[:1000]}"
        prompt_blank = f"Generate 2 fill-in-the-blank question:\n{chunk[:1000]}"
        prompt_tf = (
    f"From the following text, generate 1 complete factual statement that can be answered with 'True' or 'False'. "
    f"Make sure the statement is based on the facts in the input. Do NOT say 'True or False' in the question. "
    f"Just output the statement."
)


        mcq = generator(prompt_mcq, max_new_tokens=250)[0]['generated_text']
        blank = generator(prompt_blank, max_new_tokens=100)[0]['generated_text']
        tf = generator(prompt_tf + "\n" + chunk[:500], max_new_tokens=100)[0]['generated_text']


        mcqs.append(mcq)
        blanks.append(blank)
        tfs.append(tf)
    return mcqs, blanks, tfs

# Gemini formatting

genai.configure(api_key="AIzaSyD2eAxoxxC_J3ZMA-zbsS2qq3B1M1PY5fs")
model_gemini = genai.GenerativeModel("gemini-1.5-flash-latest")

def format_quiz(mcqs, blanks, tfs):
    prompt = f"""
    Format the following questions as a clean, interactive quiz:

    Multiple Choice Questions:
    {"\n".join(mcqs)}

    Fill in the Blanks:
    {"\n".join(blanks)}

    True/False:
    {"\n".join(tfs)}
    """
    response = model_gemini.generate_content(prompt)
    return response.text

# Main quiz generation pipeline
def generate_quiz_from_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    vectorstore, chunks = create_vectorstore(text)
    mcqs, blanks, tfs = generate_questions(chunks)
    formatted_quiz = format_quiz(mcqs, blanks, tfs)
    return formatted_quiz
