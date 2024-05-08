#!/usr/bin/env python
# coding: utf-8


# This code implements the translation of documents with .docx and .pdf formats using Streamlit, PyPDF2, deep-translator, reportlab and python-docx libraries.
# It allows users to upload a PDF or word file, extract text from it, and then translate it from ENGLISH to GERMAN without using any LLMs
# User can download the translated document using DOWNLOAD button at Streamlit interface.

import streamlit as st
from googletrans import Translator
import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)    
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text


def translate_text(text, source_lang='en', target_lang='de'):
  """
  Translates text using the googletrans library.

  Args:
      text (str): The text to be translated.
      source_lang (str, optional): The source language code. Defaults to 'en' (English).
      target_lang (str, optional): The target language code. Defaults to 'de' (German).

  Returns:
      str: The translated text.
  """

  translator = Translator()
  translation = translator.translate(text, src=source_lang, dest=target_lang)
  return translation.text


def main():
    st.title('📝 Translation Application for Documents [English to German]')
    
    # Upload file
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension.lower() == '.pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension.lower() == '.docx':
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format")
            return
        
        translated_text = translate_text(text)
        st.download_button(label="SUBMIT", data=translated_text, file_name='translated_document.txt', help='Submit File for Translation')

if __name__ == '__main__':
    main()
