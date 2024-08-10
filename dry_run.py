import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceInstructEmbeddings
#from langchain_community.embeddings import OpenAIEmbeddings  
from sentence_transformers import SentenceTransformer  # type: ignore
#from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.chroma import Chroma
import chromadb


from langchain.memory import ConversationBufferMemory
from langchain.chains.retrieval_qa.base import RetrievalQA
#from transformers import pipeline  # type: ignore
#from langchain.retrievers import MultiVectorRetriever


#from langchain.chat_models import ChatOpenAI

#os.environ['HF_HOME'] = r'E:\doc-support'
import os
os.environ['HF_HOME'] = 'E:\\doc-support'

def get_raw(corpus):
    text=''
    for pdf in corpus: 
        reader = PdfReader(pdf)
        for pages in reader.pages:
            text += pages.extract_text()
    return text
def get_chunks(raw_text):
    splitter = CharacterTextSplitter(separator="\n", 
                                     chunk_size = 1000, 
                                     chunk_overlap = 200, 
                                     length_function = len)
    return splitter.split_text(raw_text)

def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient('chroma_db')

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name='pdfs',
        embedding_function=embeddings,
    )

    return langchain_chroma

#@st.cache_resource
def get_embeddings(chunks):
    #embeddings = OpenAIEmbeddings()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", 
                                cache_folder=r'E:\doc-support\models')
    #embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    embeddings = model.encode(chunks, 
                              show_progress_bar = True)
    #db = FAISS.from_texts(texts=chunks, embedding=embeddings)
    
    #------------------#
    
    #dimension = embeddings.shape[1] 
    return embeddings
    
# def get_conversation_chain(vectorstore):
#     llm = pipeline("text-generation", model="distilgpt2")

#     def llm_function(prompt):
#         result = llm(prompt, max_length=150, num_return_sequences=1)
#         return result[0]['generated_text']
    
#     memory = ConversationBufferMemory(
#         memory_key= 'chat_history',
#         return_messages=True
#     )

#     retriever = MultiVectorRetriever(vectorstore)
#     conversation_chain = RetrievalQA.from_llm(
#         llm = llm_function(),
#         retriever = retriever,
#         memory=memory

#     )
#     return conversation_chain






def main():
    load_dotenv()
    st.set_page_config(page_title="DOC SUPPORT", 
                       page_icon=':books:')
    st.header("DOC SUPPORT :books:")
    st.text_area("Ask question")
    with st.sidebar:
        st.subheader("Upload .pdf docs")
        corpus = st.file_uploader('upload here', 
                                  label_visibility='hidden', 
                                  accept_multiple_files=True, type='pdf')
        if st.button("Process"):
            with st.spinner("Extracting contents of pdfs"):
                raw_text = get_raw(corpus)
                #st.write(raw_text)

            with st.spinner("Processing text chunks"):
                text_chunks = get_chunks(raw_text)
                
                

            with st.spinner("Creating vector embeddings"):
                # vector_store = get_embeddings(text_chunks)
                # st.write(vector_store.index.ntotal)
                embeddings = get_embeddings(text_chunks)

            with st.spinner("Creating vector db"):
                # vector_store = get_embeddings(text_chunks)
                # st.write(vector_store.index.ntotal)
                st.write(embeddings)
                vectorstore = load_vectordb(embeddings)
                st.success("Chroma vectordb successfully created!")
                
                st.write("Chunks created:", len(text_chunks))
                st.write("Embedding dimensions:", embeddings.shape[1])
                st.write(vectorstore)

            # with st.spinner("Creating conversation chain"):
            #     conversation = get_conversation_chain(vectorstore)
            #     st.write(conversation)
    

if __name__ =='__main__':
    main()