#main streamlit runner file
import streamlit as st
from dotenv import load_dotenv



def main():
    load_dotenv()
    st.set_page_config(page_title="DOC SUPPORT", page_icon=':books:')
    st.header("DOC SUPPORT :books:")
    st.text_area("Ask question")
    with st.sidebar:
        st.subheader("Upload .pdf docs")
        st.file_uploader('upload here', label_visibility='hidden')
        st.button("Process")

    

if __name__ =='__main__':
    main()