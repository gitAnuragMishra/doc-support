from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from llmchains import load_vectordb, create_embeddings
import pypdfium2 #type: ignore


def extract_text_from_pdf(pdf_bytes):
    pdf_file = pypdfium2.PdfDocument(pdf_bytes)
    return '\n'.join(pdf_file.get_page(page_number).get_textpage().get_text_range() for page_number in range(len(pdf_file)))
    
def get_pdf_texts(pdfs_bytes_list): #list of multiple pdfs
    return [extract_text_from_pdf(pdf_bytes) for pdf_bytes in pdfs_bytes_list] #return as a list

def get_text_chunks(raw_text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
        separators=['\n\n', '\n' , " ", ""]
    )
    return splitter.split_text(raw_text)

def get_document_chunks(text_list : list):
    doc = []
    for text in text_list:
        for chunk in get_text_chunks(text):
            doc.append(Document(page_content = chunk))
    return doc #as a list



def add_pdf_to_db(pdfs_bytes):
    texts = get_pdf_texts(pdfs_bytes)
    documents = get_document_chunks(texts)
    vector_db = load_vectordb(create_embeddings())
    vector_db.add_documents(documents)
    
    return 