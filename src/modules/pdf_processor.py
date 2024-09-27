import fitz
import streamlit as st
from utils.text_splitter import split_text

def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = []
        for page_num in range(len(doc)):
            try:
                page = doc.load_page(page_num)
                text.append(page.get_text())
            except Exception as e:
                st.error(f"Erro ao ler a página {page_num} do PDF {file_path}: {e}")
                continue
        return "\n".join(text)
    except Exception as e:
        st.error(f"Erro ao abrir o PDF {file_path}: {e}")
        return ""

def process_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if text:
        return split_text(text, max_tokens=5000)
    else:
        return []