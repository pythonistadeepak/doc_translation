#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This code implements the translation of documents with .docx and .pdf formats using Streamlit, PyPDF2, deep-translator, reportlab and python-docx libraries.
# It allows users to upload a PDF or word file, extract text from it, and then translate it from ENGLISH to GERMAN without using any LLMs
# User can download the translated document using DOWNLOAD button at Streamlit interface.


# In[ ]:


# !pip install streamlit
# !pip install googletrans==3.1.0a0
# !pip install PyPDF2
# !pip install python-docx

# !pip install reportlab==4.2.0


# In[ ]:





# In[1]:


import streamlit as st
from googletrans import Translator
import os
# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
from docx import Document


# In[2]:


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)    
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


# In[3]:


def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text


# In[4]:


# text = extract_text_from_docx("ARTICLE - Critical Parameters to Monitor for Deployed AI Models - ORGINAL.docx")
# msg_pdf = extract_text_from_pdf("ARTICLE - Critical Parameters to Monitor for Deployed AI Models.pdf")


# In[ ]:





# In[5]:


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


# In[ ]:





# In[7]:





# In[ ]:


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
#         st.write("Translated text TESTING:")
#         st.write(translated_text)
        st.download_button(label="SUBMIT", data=translated_text, file_name='translated_document.txt', help='Submit File for Translation')

if __name__ == '__main__':
    main()


# In[ ]:




