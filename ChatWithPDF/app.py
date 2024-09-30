import streamlit as st  # Streamlit library ko import kar rahe hain, jo web app banane ke liye hai.
from PyPDF2 import PdfReader  # PyPDF2 se PdfReader ko import karte hain taaki PDF se text extract kar sakein.
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Langchain se text splitter import karte hain jo text ko chunks mein divide karega.
import os  # Operating system se related functions ke liye os module ko import karte hain.
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Google Generative AI ke embeddings ko use karne ke liye import karte hain.
import google.generativeai as genai  # Google generative AI ko import karte hain.
from langchain.vectorstores import FAISS  # FAISS ko import karte hain, jo vector store ke liye hai.
from langchain_google_genai import ChatGoogleGenerativeAI  # Chat model ko import karte hain jo conversation ke liye use hoga.
from langchain.chains.question_answering import load_qa_chain  # Question answering chain ko load karne ke liye import karte hain.
from langchain.prompts import PromptTemplate  # Prompt template ko import karte hain, jo AI model ko questions dene mein madad karega.
from dotenv import load_dotenv  # .env file se environment variables load karne ke liye import karte hain.

load_dotenv()  # .env file se environment variables ko load karte hain.
os.getenv("GOOGLE_API_KEY")  # Google API key ko environment se fetch karte hain.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Google AI ko configure karte hain API key ke saath.

# PDF se text extract karne ka function
def get_pdf_text(pdf_docs):
    text = ""  # Text ko store karne ke liye ek empty string banate hain.
    for pdf in pdf_docs:  # Har uploaded PDF document par iterate karte hain.
        pdf_reader = PdfReader(pdf)  # PDF ko read karne ke liye PdfReader ka instance banate hain.
        for page in pdf_reader.pages:  # PDF ke har page par iterate karte hain.
            text += page.extract_text()  # Page se text extract karte hain aur string mein add karte hain.
    return text  # Final text ko return karte hain.

# Text ko chunks mein divide karne ka function
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)  # Text splitter ka instance banate hain.
    chunks = text_splitter.split_text(text)  # Text ko chunks mein divide karte hain.
    return chunks  # Chunks ko return karte hain.

# Vector store create karne ka function
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Google AI ke embeddings create karte hain.
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)  # Text chunks ke liye vector store banate hain.
    vector_store.save_local("faiss_index")  # Vector store ko local storage mein save karte hain.

# Conversational chain setup karne ka function
def get_conversational_chain():
    prompt_template = """  # Prompt template ko define karte hain.
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)  # Chat model ka instance banate hain.
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])  # Prompt template banate hain.
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)  # Question answering chain ko load karte hain.

    return chain  # Chain ko return karte hain.

# User ka question process karne ka function
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Embeddings create karte hain.

    new_db = FAISS.load_local("faiss_index", embeddings)  # Local vector store ko load karte hain.
    docs = new_db.similarity_search(user_question)  # User ke question ke liye similar documents ko search karte hain.

    chain = get_conversational_chain()  # Conversational chain ko get karte hain.

    response = chain(  # Chain ko call karte hain taaki response generate ho.
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    print(response)  # Response ko print karte hain (console mein).
    st.write("Reply: ", response["output_text"])  # Streamlit app mein response ko display karte hain.

# Main function to run the app
def main():
    st.set_page_config("Chat PDF")  # Streamlit app ka page configuration set karte hain.
    st.header("Chat with PDF using Gemini💁")  # App ka header set karte hain.

    user_question = st.text_input("Ask a Question from the PDF Files")  # User se question lene ke liye input box.

    if user_question:  # Agar user ne question diya hai.
        user_input(user_question)  # User input function ko call karte hain.

    with st.sidebar:  # Sidebar section banate hain.
        st.title("Menu:")  # Sidebar ka title set karte hain.
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)  # PDF upload karne ka option dete hain.
        if st.button("Submit & Process"):  # Agar user ne button click kiya.
            with st.spinner("Processing..."):  # Processing spinner dikhate hain.
                raw_text = get_pdf_text(pdf_docs)  # Uploaded PDFs se text extract karte hain.
                text_chunks = get_text_chunks(raw_text)  # Extracted text ko chunks mein convert karte hain.
                get_vector_store(text_chunks)  # Chunks ko vector store mein save karte hain.
                st.success("Done")  # Processing complete hone par success message dikhate hain.

# Agar script directly run ki gayi hai, to main function ko call karte hain.
if __name__ == "__main__":
    main()
