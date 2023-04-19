import streamlit as st
import io
from pdf2image import convert_from_bytes
from PIL import Image

from langchain.embeddings import LlamaCppEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain import OpenAI
from langchain.chains import RetrievalQA 
from langchain.llms import OpenAIChat
from langchain.document_loaders import PagedPDFSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import PyPDF2
import base64
import urllib
chat_history = []
st.set_page_config(layout="wide")
def displayPDF(file):
    # Opening file from file path. this is used to open the file from a website rather than local
    
    
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="700" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    
# Function to extract text from PDF
def extract_text_from_pdf(uploaded_pdf):
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num]. extract_text()
            
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0,separator="\n")
    texts = text_splitter.split_text(text)
    # embeddings = OpenAIEmbeddings(openai_api_key="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")
    # embeddings = LlamaCppEmbeddings(model_path="ggml-model-q4_0.bin")
    embeddings = HuggingFaceEmbeddings()

    db = FAISS.from_texts(texts, embeddings)
    
        
    return db

# Function to process user input and provide a response
def get_answer(question, context):
    
    qa = RetrievalQA.from_chain_type(llm=OpenAI(model='text-davinci-003',openai_api_key="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"), chain_type='stuff', retriever=context.as_retriever())
    ans = qa.run(question)

    
    
    return ans

st.title("PDF Chatbot")

# Create columns
left_column, right_column = st.columns([2,5])

# PDF upload and preview in left column
with left_column:
    st.write("Upload a PDF and ask any question from the content.")
    uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    # 
    # Show first page preview if the PDF is uploaded
    if uploaded_pdf is not None:
        displayPDF(uploaded_pdf)

       
    else:
        st.warning("Please upload a PDF file.")

# Chat UI in right column


with right_column:
    if uploaded_pdf is not None:
        # Initialize chat history
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            

        # Display chat history
        st.subheader("Chat History")
        for i, chat in enumerate(st.session_state.chat_history, 1):
            st.write(f"Q{i}: {chat['question']}")
            st.write(f"A{i}: {chat['answer']}")
            

        user_question = st.text_input("Type your question here:")
        submit_button = st.button("Submit")
        

        if submit_button and user_question:
            answer = get_answer(user_question,extract_text_from_pdf(uploaded_pdf) )
            chat = {"question": user_question, "answer": answer}
            st.session_state.chat_history.append(chat)
            st.write("Answer:", answer)

