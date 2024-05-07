#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from googletrans import Translator
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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


def generate_pdf(text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, text)
    pdf.save()
    buffer.seek(0)
    return buffer


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
        st.write("Translated text:")
        st.write(translated_text)

        st.write("Download translated PDF:")
        with st.spinner('Generating PDF...'):
            output_file = generate_pdf(translated_text)
        st.download_button(label="Download", data=output_file, file_name='translated_document.pdf', mime='application/pdf', key='download-pdf')

if __name__ == '__main__':
    main()
