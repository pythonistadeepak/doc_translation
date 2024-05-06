# This code implements the translation of documents with .docx and .pdf formats using Streamlit, PyPDF2, deep-translator, reportlab and python-docx libraries.
# It allows users to upload a PDF or word file, extract text from it, and then translate it from ENGLISH to GERMAN without using any LLMs
# User can download the translated document using DOWNLOAD button at Streamlit interface.

import streamlit as st
from deep_translator import GoogleTranslator
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader
from docx import Document



import streamlit as st
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import os

# Function to summarize text
def summarize_text(texts, docsearch, chain):
    # """
    # This function takes a list of texts, a document search object, and a question answering chain as input.
    # It performs text summarization by using the document search object to find the most similar document to an empty query,
    # and then passes the document to the question answering chain with a predefined question asking for a summary within 150 words.
    # The summarized text is returned as output.
    # """
    summry = docsearch.similarity_search(" ")  # Find most similar document to empty query
    txt = chain.run(input_documents=summry, question="write summery in points within 150 words")  # Run question answering chain
    return txt


# Function to answer question
def answer_question(query, docsearch, chain):
    # """
    # This function takes a query, a document search object, and a question answering chain as input.
    # It performs question answering by using the document search object to find the most similar documents to the input query,
    # and then passes the documents to the question answering chain with the input query as the question.
    # The answer to the question is returned as output.
    # """
    docs = docsearch.similarity_search(query)  # Find most similar documents to input query
    txt = chain.run(input_documents=docs, question=query)  # Run question answering chain
    return txt

# Main function
def main():
    # """
    # This is the main function that runs the Streamlit application.
    # It displays a title, allows users to input their API key, upload a PDF file, and input additional text for analysis.
    # It also allows users to input a document for translation to German Language.
    # The function calls the summarize_text() and answer_question() functions to perform text summarization and question answering
    # respectively, and displays the results using Streamlit interface.
    # """
    st.title('📝 Translation Application for Documents')

    api_key = st.text_input('Your OpenAI Key', placeholder="Enter Your key")
    os.environ["OPENAI_API_KEY"] = api_key

    raw_text = ''

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text

    temp_data = "data : "
    temp_data += st.text_area('Text to analyze', placeholder="Enter Your Data")

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    texts = text_splitter.split_text(raw_text)
    texts.append(temp_data)

    query = "query : "
    query += st.text_area('Query on Data', placeholder="Enter Your Query")

    col1, col2, col3 = st.columns(3)

    # Button click event and input validation
    if col2.button('Submit') and (uploaded_file is not None or temp_data!="data : "):
        if api_key=="":
            st.warning('Enter the OpenAI API Key', icon="⚠️")
        else:
            embeddings = OpenAIEmbeddings()
            docsearch = FAISS.from_texts(texts, embeddings)
            chain = load_qa_chain(OpenAI(), chain_type="stuff")

            # Streamlit session state usage
            if 'summry' not in st.session_state or  query == "query : ":
                # """
                # This condition checks if the 'summry' key is not present in the Streamlit session state, or if the input query is empty.
                # If either of these conditions is true, it means that the summary is not computed yet or the user has cleared the query input.
                # In such cases, the summarize_text() function is called to compute the summary and store it in the 'summry' key of the session state.
                # """
                # Call summarize_text() function
                st.session_state['summry'] = summarize_text(texts, docsearch, chain)
                st.write('Summary:', st.session_state['summry'])

            # Call answer_question() function
            if query != "query : ":
                txt = answer_question(query, docsearch, chain)
                st.write('Output:', txt)
    else:
        st.write('Enter Your Query !')

if __name__ == '__main__':
    main()
