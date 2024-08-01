import streamlit as st
from llmchains import load_normal_chain   


def load_chain():
    return load_normal_chain()

def set_send_input():
    st.session_state.send_input = True
    clear_input()

def clear_input():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ' '

def main():
    st.set_page_config(page_title="Doc Support", 
                       page_icon=':books:')
    st.header("DOC SUPPORT :books:")

    if 'send_input' not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ' '

    chat_container = st.container()
    user_input = st.text_area("ask your question", key = 'user_input' , on_change=set_send_input)
    send_button = st.button("Process", key = 'send_button')

    
    if send_button or st.session_state.send_input:
        if st.session_state.user_question != ' ':
            llm_response = "hello world" 

            with chat_container:
                with st.chat_message('user', avatar= 'human'):
                    st.write(st.session_state.user_question)    #one way of writing code
                    
                st.chat_message('llm', avatar= 'ai').write('llm_response') #another way
    


if __name__ =='__main__':
    main()