import os
from docx import Document
import PyPDF2
import pandas as pd
from groq import Groq
from config_loader import load_config
from time import sleep

# Config setup
config = load_config()

MAX_WORDS = config.get('max_word', 1000)
GROQ_API_KEY = config.get('groq_api_key', '')
MODEL = config.get('groq_llm')
PROMPT = config.get('prompt')
SLEEP = config.get('sleep')

# Set up Groq client
client = Groq(api_key=GROQ_API_KEY)

def read_file(file_path):
    """Reads the content of the file based on its extension."""
    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.txt':
        return read_txt(file_path)
    elif extension == '.docx':
        return read_docx(file_path)
    elif extension == '.pdf':
        return read_pdf(file_path)
    elif extension in ['.xls', '.xlsx', '.csv']:
        return read_excel_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: '{extension}'")

def read_txt(file_path):
    """Reads text files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx(file_path):
    """Reads DOCX files."""
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def read_pdf(file_path):
    """Reads PDF files."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to read PDF file '{file_path}': {e}")

def read_excel_csv(file_path):
    """Reads Excel or CSV files using pandas."""
    try:
        df = pd.read_excel(file_path) if file_path.endswith(('.xls', '.xlsx')) else pd.read_csv(file_path)
        return df.to_string(index=False)
    except Exception as e:
        raise RuntimeError(f"Error reading Excel/CSV file '{file_path}': {e}")

def preprocess_text(text):
    """Cleans and removes unnecessary whitespace from text."""
    return ' '.join(text.split())

def chunk_text(text):
    """Splits the text into chunks based on the MAX_WORDS limit."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= MAX_WORDS:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def summarize_with_groq(text, chunk=1):
    """Uses Groq's API to summarize text chunks."""
    if (MAX_WORDS > 5000):
        print(f"[INFO] Initiating sleep {SLEEP}sec to prevent API rate limiting issues.")
        sleep(SLEEP)
    try:
        messages = [
            {"role": "system", "content": PROMPT.format(chunk_number=chunk, document_chunk=text)},
            {"role": "user", "content": "Summarize the document"}
        ]
        response = client.chat.completions.create(model=MODEL, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"[ERROR] {e}")

def summarize_file(file_path):
    """Summarizes the content of a file."""
    try:
        raw_text = read_file(file_path)
    except ValueError as e:
        print(f"[ERROR] {e}")
        return ""
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        return ""

    cleaned_text = preprocess_text(raw_text)
    chunks = chunk_text(cleaned_text)

    summaries = []
    for index, chunk in enumerate(chunks):
        try:
            summary = summarize_with_groq(chunk, index + 1)
            summaries.append(summary)
            print(f"[SUCCESS] Summarized chunk {index + 1}/{len(chunks)} successfully.")
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            summaries.append("")

    combined_summary = ' '.join(summaries).strip()
    return combined_summary
