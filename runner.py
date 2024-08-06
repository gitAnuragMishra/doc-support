import streamlit as st
from llmchains import load_normal_chain 
from utility import save_chat_history_json, load_chat_history_json, get_timestamp
from langchain.memory import StreamlitChatMessageHistory
import torch
import yaml
import os
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
            st.session_state.new_session_key = get_timestamp()
            save_chat_history_json(st.session_state.history, config['chat_history_path'] + st.session_state.new_session_key + ".json")
        else:
            save_chat_history_json(st.session_state.history, config['chat_history_path'] + st.session_state.session_key + ".json")

def main():
    st.set_page_config(page_title="Doc Support", 
                       page_icon=':books:')
    st.header("Doc Support :books:", divider=True)

    st.sidebar.title("Chat Sessions")
    chat_sessions = ['new_session'] + os.listdir(config['chat_history_path'])
    st.sidebar.selectbox("Select the chat session", chat_sessions, key='session_key')

    if 'send_input' not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ' '
        st.session_state.new_session_key = None


    

    

    chat_history = StreamlitChatMessageHistory(key='history')
    llm_chain = load_chain(chat_history)
    chat_container = st.container(border=True)
    user_input = st.text_area(label='question', label_visibility='hidden', placeholder="ask your question", key = 'user_input' , on_change=set_send_input)
    send_button = st.button("Process", key = 'send_button')

    
    if send_button or st.session_state.send_input:
        if st.session_state.user_question != ' ':
            llm_response = llm_chain.run(user_input=st.session_state.user_question) 
            
            with chat_container:
                # with st.chat_message('user', avatar= 'human'):
                #     st.write(st.session_state.user_question)    #one way of writing code
                    
                #st.chat_message('llm', avatar= 'ai').write(llm_response) #another way
                st.session_state.user_question != ' '
                
        if chat_history.messages != []:
            with chat_container:
                st.write("Chat History: ")
                for message in chat_history.messages:
                    st.chat_message(message.type).write(message.content)
        del llm_response
        torch.cuda.empty_cache()

    save_chat_history()
    


if __name__ =='__main__':
    main()