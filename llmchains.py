from langchain.chains import LLMChain
# from langchain.chains import StuffDocumentsChain, ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms.ctransformers import CTransformers
from langchain_community.vectorstores.chroma import Chroma
import chromadb
from prompt_template import memory_prompt_template
import yaml
import torch
# from accelerate import Accelerator #type: ignore
from sentence_transformers import SentenceTransformer #type: ignore
#from transformers import AutoModelForCausalLM
#from llama_cpp import Llama
import os
os.environ['HF_HOME'] = r'D:\models'
os.environ['HF_HUB_CACHE'] = r'D:\models'
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)




def create_embeddings(embeddings_path = config['embeddings_path']):
    embedding_model = HuggingFaceBgeEmbeddings(model_name = embeddings_path, cache_folder=r'D:\models')
    #embedding_model = SentenceTransformer(model_name_or_path='D:\models\models--sentence-transformers--all-MiniLM-L6-v2', cache_folder=r'D:\models')
    return embedding_model
def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient(path = 'chroma_db')

    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name="pdf_store",
        embedding_function=embeddings,
    )
    return vector_store_from_client


def create_llm(model_path = config['tinyllama_model']['model_path'], model_type = config['tinyllama_model']['model_type'], model_config = config['tinyllama_model']['model_config'], gpu_layers= config['tinyllama_model']['model_config']['gpu_layers']):
    
    llm = CTransformers(model=model_path, model_type= model_type, config=model_config, gpu_layers = gpu_layers)

        
    #llm = CTransformers(model_path='models\gpt2_pytorch_model.bin', model_type= 'gpt2', gpu_layers = 10)
    return llm

def create_chat_memory(chat_history):
    return ConversationBufferWindowMemory(memory_key= "history", chat_memory=chat_history, k = 3)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def create_llm_chain(llm, chat_prompt, memory):
    return LLMChain(llm=llm, prompt= chat_prompt, memory=memory)

def load_normal_chain(chat_history):
    return chatChain(chat_history)

def load_vectordb_chain(chat_history):
    return pdfChatChain(chat_history)

def load_retrieval_chain(llm, memory, vectordb):
    return RetrievalQA.from_llm(llm=llm, retriever=vectordb.as_retriever(), memory=memory)


class chatChain:
    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm()
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain= create_llm_chain(llm, chat_prompt, self.memory)

    # def invoke(self, user_input):
    #     return self.llm_chain.invoke(user_input)
    # {
#   "human_input": " are you ready",
#   "history": "",
#   "text": "1. Yes, I am ready to assist you with any questions or concerns you may have. How can I help you today?"
# }

    def run(self, user_input):
        #return self.llm_chain.invoke(user_input, stop = ['Human:'])
        print('Normal chat running')
        return self.llm_chain.run(human_input = user_input, history = self.memory.chat_memory.messages, stop = ['Human:'])


class pdfChatChain:
    def __init__(self, chat_history):
        self.memory = create_chat_memory(chat_history)
        self.vectordb = load_vectordb(create_embeddings())
        llm = create_llm()
        #chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain= load_retrieval_chain(llm, self.memory, self.vectordb)

    def run(self, user_input):
        print('Pdf chat running')
        return self.llm_chain.run(query = user_input, history = self.memory.chat_memory.messages, stop = ['Human:'])