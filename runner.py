import streamlit as st
from llmchains import load_normal_chain 
from utility import save_chat_history_json, load_chat_history_json, get_timestamp
from langchain.memory import StreamlitChatMessageHistory
import torch
import yaml
import os
from pdf_handler import add_pdf_to_db
# import atexit
# import shutil
# import time

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def load_chain(chat_history):
    return load_normal_chain(chat_history)

def set_send_input():
    st.session_state.send_input = True
    clear_input()

def clear_input():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ' '

def save_chat_history():
    if st.session_state.history != []:
        if st.session_state.session_key == 'new_session':
            st.session_state.new_session_key = get_timestamp() + '.json'
            save_chat_history_json(st.session_state.history, config['chat_history_path'] + st.session_state.new_session_key)
        else:
            save_chat_history_json(st.session_state.history, config['chat_history_path'] + st.session_state.session_key)


    



def main():
    st.set_page_config(page_title="Doc Support", page_icon=':books:')
    st.header("Doc Support :books:", divider=True)

    


    st.sidebar.title("Chat Sessions")
    chat_sessions = ['new_session'] + os.listdir(config['chat_history_path'])

    #initialising session state variables
    if 'send_input' not in st.session_state:
        st.session_state.session_key = 'new_session'
        st.session_state.send_input = False
        st.session_state.user_question = ' '
        st.session_state.new_session_key = None
        st.session_state.session_index_tracker = 'new_session'
        st.session_state.history_loaded = False 
        st.session_state.pdf_uploader_key = 1

    if st.session_state.session_key == 'new_session' and st.session_state.new_session_key != None:
        st.session_state.session_index_tracker = st.session_state.new_session_key
        st.session_state.new_session_key = None

    index = chat_sessions.index(st.session_state.session_index_tracker)
    selected_session = st.sidebar.selectbox("Return to chats", chat_sessions, key='session_key', index=index)
    
    if st.session_state.session_key != 'new_session':
        st.session_state.history = load_chat_history_json(config['chat_history_path'] + st.session_state.session_key)
    
    uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type="pdf", accept_multiple_files=True, key=st.session_state.pdf_uploader_key)

    if uploaded_pdf:
        with st.sidebar:
            with st.spinner('Adding pdf to vector db...'):
                add_pdf_to_db(uploaded_pdf)
                st.session_state.pdf_uploader_key += 2
                st.success('PDF added')
    
    
    

    # Automatically load chat history once a session is selected
    if selected_session != 'new_session' and not st.session_state.history_loaded:
        st.session_state.history = load_chat_history_json(config['chat_history_path'] + selected_session)
        st.session_state.history_loaded = True

    chat_history = StreamlitChatMessageHistory(key='history')
    llm_chain = load_chain(chat_history)
    chat_container = st.container(border=True)
    user_input = st.text_area(label='question', label_visibility='hidden', placeholder="Ask your question", key='user_input', on_change=set_send_input)
    send_button = st.button("Process", key='send_button')

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != ' ':
            with st.spinner('Generating response...'):
                llm_response = llm_chain.run(user_input=st.session_state.user_question)
                with chat_container:
                    # with st.chat_message('user', avatar='human'):
                    #     st.write(st.session_state.user_question)  # One way of writing user question.

                    # st.chat_message('llm', avatar='ai').write(llm_response)  # Another way to write LLM response.
                    pass  # This is where you handle user questions.


    if chat_history.messages != []:
        with chat_container:
            st.write("Chat History: ")
            for message in chat_history.messages:
                with st.spinner('Generating response...'):
                    st.chat_message(message.type).write(message.content)
        torch.cuda.empty_cache()

    save_chat_history()
    # def cleanup_vector_db_folder():  #clear all contents of vector db
    #     ##to be noted: having this function out of the main funtion causes a permission error 
    #     time.sleep(2)  # time to release 
    #     if os.path.exists(config['vector_db_path']):
    #         for root, dirs, files in os.walk(config['vector_db_path']):
    #             for file in files:
    #                 try:
    #                     os.remove(os.path.join(root, file))
    #                 except Exception as e:
    #                     print(f"Error deleting file {file}: {e}")
    #             for dir in dirs:
    #                 try:
    #                     shutil.rmtree(os.path.join(root, dir))
    #                 except Exception as e:
    #                     print(f"Error deleting directory {dir}: {e}")
    #         print(f"Cleared contents of vector DB folder: {config['vector_db_path']}")

    
    
    # atexit.register(cleanup_vector_db_folder)



    


if __name__ =='__main__':
    main()