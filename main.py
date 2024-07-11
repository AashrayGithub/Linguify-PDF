import os
import streamlit as st
import openai
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key  # Set the API key for OpenAI

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

st.title("PDF to English Text Converter")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    if st.button("Convert to English Text"):
        # Translate text to English using text-davinci-003
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Translate the following text to English:\n\n{pdf_text}",
            max_tokens=2048
        )
        
        translated_text = response['choices'][0]['text'].strip()
        
        st.write("**Translated Text:**")
        st.write(translated_text)
