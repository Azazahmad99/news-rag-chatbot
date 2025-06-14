import os
import streamlit as st 
from langchain_groq import ChatGroq 
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from data_injection import get_news_link, extract_all_links, formatted_date
from data_injection import news_collection_from_url

@st.cache_resource
def setup_rag_pipeline(file_path, groq_api_key, llm):
    # 1. Load the text data
    loader = TextLoader(file_path)
    documents = loader.load()

    # 2. Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Create the vector store (ChromaDB)
    db = Chroma.from_documents(chunks, embeddings)
    retriever = db.as_retriever(search_kwargs={'k': 3})

    # 5. Set up the Groq LLM
    llm_model = ChatGroq(model_name=llm, groq_api_key=groq_api_key)

    # 6. Set up memory for chat history
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)

    # 7. Create the prompt template with history
    prompt_template = """
    You are an intelligent assistant that answers questions based on the latest news content. 
    The context contains multiple news articles. Your job is to find relevant information and respond clearly, accurately, and engagingly.

    Instructions:
    - Present the answer in well-structured bullet points.
    - Use bold text for important keywords, names, or dates if supported.
    - Summarize concisely while keeping the answer informative and attractive.
    - Avoid repeating or irrelevant content.

    📌 Context (News Data):
    {context}

    📜 Chat History:
    {history}

    ❓ Question:
    {question}

    ✅ Your Response:
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 8. Create the RAG chain with memory
    rag_chain_with_history = (
        {"context": retriever, "question": RunnablePassthrough(), "history": lambda x: memory.load_memory_variables(x)['history']}
        | prompt
        | llm_model
        | StrOutputParser()
    )
    return rag_chain_with_history, memory
