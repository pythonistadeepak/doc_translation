#!/usr/bin/env python

"""
Program Name: Language Translation
Purpose     : This code implements the translation of documents with .docx and .pdf formats.
              It uses Streamlit for the web interface, PyPDF2 for handling PDFs, 
              googletrans for translation (English to German), and python-docx for handling Word documents.
              
# Functionality:
#  - Users upload a PDF or Word document.
#  - The application extracts text from the uploaded document.
#  - The extracted text is translated from English to German.
#  - Users can download the translated text as a TXT file.

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Deepak Kumar         ##8th May,2024        ##V0.1                ##
        ##------------------------------------------------------------------##
        ######################################################################

"""


import streamlit as st
from googletrans import Translator
import os
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (file object): The uploaded PDF file object.

    Returns:
        str: The extracted text from the PDF.
    """
    reader = PdfReader(pdf_file)    
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def extract_text_from_docx(docx_file):
    """
    Extracts text from a Word document (.docx).

    Args:
        docx_file (file object): The uploaded Word document object.

    Returns:
        str: The extracted text from the Word document.
    """
    doc = Document(docx_file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text


def translate_text(text, source_lang='en', target_lang='de'):
    """
    Translates text from source language to target language.

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
    """
    Main function to run the Streamlit application.
    """
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
