import streamlit as st


def main():
    st.set_page_config(page_title="Doc Support", 
                       page_icon=':books:')
    st.header("DOC SUPPORT :books:")


    chat_container = st.container()
    user_input = st.text_area("ask your question", key = 'user_input' )
    send_button = st.button("Process", key = 'send_button')

    llm_response = '...'
    if send_button:
        llm_response = "hello world" 

    with chat_container:
        with st.chat_message('user', avatar= 'human'):
            st.write(user_input)    #one way of writing code
            
        st.chat_message('llm', avatar= 'ai').write(llm_response) #another way
    


if __name__ =='__main__':
    main()