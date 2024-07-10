!pip install PyMuPDF
!pip install nltk

import streamlit as st
import fitz  # PyMuPDF
from nltk.tokenize import word_tokenize
import nltk

# Download NLTK data files (run this once)
nltk.download('punkt')

def extract_content_from_abstract(file_text):
    content = []
    lines = file_text.splitlines()
    abstract_found = False
    heading_found = False

    for line in lines:
        line = line.strip()
        if line:
            words = word_tokenize(line)
            if words and len(words) <= 5 and (words[0][0].isupper() or words[0][0].isdigit()):
                if abstract_found and not heading_found:
                    heading_found = True
                elif abstract_found and heading_found:
                    break  # Stop after finding the next heading after "Abstract"
                elif words[0].lower() == 'abstract':  # Case insensitive check for "Abstract"
                    abstract_found = True
            elif abstract_found and not heading_found:
                content.append(line)

    return '\n'.join(content)

st.title("PDF Abstract Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        file_text = doc[0].get_text()

    extracted_content = extract_content_from_abstract(file_text)

    st.write("Content of Abstract")
    st.text_area("Abstract", extracted_content, height=300)
