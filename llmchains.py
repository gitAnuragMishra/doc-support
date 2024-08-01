from langchain.chains import StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceInstructEmbeddings, HuggingFaceBgeEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms.ctransformers import CTransformers
from langchain_community.vectorstores.chroma import Chroma
import chromadb
from prompt_template import memory_prompt_template
import yaml
#from sentence_transformers import SentenceTransformer
import os
os.environ['HF_HOME'] = r'E:\doc-support\models'
os.environ['HF_HUB_CACHE'] = r'E:\doc-support\models'


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def create_llm(model_path = config['model']['model_path'], model_type = config['model']['model_type']):
    llm = CTransformers(model_path, model_type)
    return llm

def create_llm_chain(embeddings_path = config['embeddings_path']):

    embedding_model = HuggingFaceBgeEmbeddings(embeddings_path)
    return embedding_model

def create_chat_memory():
    return ConversationBufferWindowMemory(memory_key= "history", chat_memory=chat_history, k = 3)

def create_prompt_from_template(template):
    return PromptTemplate.from_template(template)

def create_llm_chain(llm, chat_prompt, memory):
    return LLMChain(llm, chat_prompt, memory)

def load_normal_chain():
    return chatChain(chat_history)

class chatChain:
    def __init__(self, chat_history, model_path = config['model']['model_path'], model_type = config['model']['model_type']):
        self.memory = create_chat_memory(chat_history)
        llm = create_llm(model_path, model_type)
        chat_prompt = create_prompt_from_template(memory_prompt_template)
        self.llm_chain= create_llm_chain(llm, chat_prompt, self.memory)

