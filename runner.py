#main streamlit runner file
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
#from langchain_community.embeddings import OpenAIEmbeddings  
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

#os.environ['HF_HOME'] = r'E:\doc-support'

def get_raw(corpus):
    text=''
    for pdf in corpus: 
        reader = PdfReader(pdf)
        for pages in reader.pages:
            text += pages.extract_text()
    return text
def get_chunks(raw_text):
    splitter = CharacterTextSplitter(separator="\n", chunk_size = 1000, chunk_overlap = 200, length_function = len)
    return splitter.split_text(raw_text)

#@st.cache_resource
def get_embeddings(texts):
    #embeddings = OpenAIEmbeddings()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2', cache_folder=r'E:\doc-support')
    embeddings = model.encode(texts)
    #vector_store = FAISS.from_texts(texts, embeddings)
    # embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    #vector_store = FAISS.from_texts(texts, embeddings)
    #return vector_store
    return embeddings

def main():
    load_dotenv()
    st.set_page_config(page_title="DOC SUPPORT", page_icon=':books:')
    st.header("DOC SUPPORT :books:")
    st.text_area("Ask question")
    with st.sidebar:
        st.subheader("Upload .pdf docs")
        corpus = st.file_uploader('upload here', label_visibility='hidden', accept_multiple_files=True, type='pdf')
        if st.button("Process"):
            with st.spinner("Extracting contents of pdfs"):
                raw_text = get_raw(corpus)
                #st.write(raw_text)

            with st.spinner("Processing text chunks"):
                text_chunks = get_chunks(raw_text)
                #st.write(text_chunks)

            with st.spinner("Creating vector embeddings"):
                #vector_store = get_embeddings(text_chunks)
                #st.write(vector_store.index.ntotal)
                st.write(get_embeddings(text_chunks))

    

if __name__ =='__main__':
    main()