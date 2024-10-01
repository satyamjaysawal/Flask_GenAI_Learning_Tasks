import streamlit as st  # Streamlit ko import karte hain jo hamari web app banane mein madad karta hai
import os  # OS module ko import karte hain taaki environment variables aur file handling kiya ja sake
from langchain_groq import ChatGroq  # ChatGroq ko import karte hain jo LLM (Language Learning Model) ko query karne mein use hota hai
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Text ko chunks mein divide karne ke liye text splitter import kar rahe hain
from langchain.chains.combine_documents import create_stuff_documents_chain  # Document chain banane ke liye function import kar rahe hain
from langchain_core.prompts import ChatPromptTemplate  # ChatPromptTemplate ko import kar rahe hain taaki prompt define kar sakein
from langchain.chains import create_retrieval_chain  # Retrieval chain ko create karne ke liye function import kar rahe hain
from langchain_community.vectorstores import FAISS  # FAISS ko import karte hain jo vector search engine hai, embeddings handle karta hai
from langchain_community.document_loaders import PyPDFDirectoryLoader  # PDF documents ko load karne ke liye PDF loader import kar rahe hain
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Google Generative AI ke embeddings ko use karne ke liye yeh module import karte hain
from dotenv import load_dotenv  # Environment variables load karne ke liye dotenv ko import kar rahe hain

# Environment variables ko load karne ke liye
load_dotenv()

# GROQ aur Google API keys ko load kar rahe hain
groq_api_key = os.getenv('GROQ_API_KEY')  # GROQ API key ko .env file se load karte hain
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # Google API key ko environment variable mein set karte hain

# Streamlit app ka title set karte hain
st.title("Gemma Model Document Q&A")

# ChatGroq instance ko initialize karte hain Llama3-8b model ke saath
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Prompt template define kar rahe hain jisme context aur user ka question rahega
prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question.
<context>
{context}
<context>
Questions:{input}
"""
)

# Vector embedding function jo PDFs ko vector space mein convert karega
def vector_embedding():
    if "vectors" not in st.session_state:  # Agar vector store pehle se nahi hai to naye embeddings generate karte hain
        # Google ke embeddings ka model load karte hain
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Directory se PDF files ko load karte hain
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")  # "./us_census" folder se PDFs ko load kar rahe hain
        
        # PDFs ko load karke documents mein convert karte hain
        st.session_state.docs = st.session_state.loader.load()  # PDFs ko load kar rahe hain
        
        # Text splitter ko initialize karte hain jo text ko 1000 characters ke chunks mein divide karega
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        # 20 documents ko chunk mein split karte hain taaki process kar sakein
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        
        # Final documents ke embeddings ko FAISS vector store mein store karte hain
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# User ke question ke liye input field
prompt1 = st.text_input("Enter Your Question From Documents")  # User se question input field mein le rahe hain

# Agar user "Documents Embedding" button click kare to vector store ko generate karte hain
if st.button("Documents Embedding"):
    vector_embedding()  # Vector embedding process ko run karte hain
    st.write("Vector Store DB Is Ready")  # User ko batate hain ki vector store ready hai

# Jab user koi question input karta hai
if prompt1:
    # Document chain banate hain jo context ke according question ko answer karega
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Vector store se retriever ko load karte hain jo similar documents ko search karega
    retriever = st.session_state.vectors.as_retriever()
    
    # Document retriever aur LLM ke beech ek retrieval chain banate hain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # Process start karte hain aur time note karte hain taaki response time track kiya ja sake
    start = time.process_time()
    
    # Retrieval chain ko call karte hain taaki user ka input process kiya ja sake
    response = retrieval_chain.invoke({'input': prompt1})
    
    # Response ka time calculate karte hain
    print("Response time:", time.process_time() - start)
    
    # User ko model ka jawab dikhate hain
    st.write(response['answer'])

# Document similarity search results ko dikhane ke liye expander ka use karte hain
with st.expander("Document Similarity Search"):
    # Relevant documents ko loop karke dikhate hain
    for i, doc in enumerate(response["context"]):
        st.write(doc.page_content)  # Document ka content display karte hain
        st.write("--------------------------------")  # Line separator dikhate hain
