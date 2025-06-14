import os
import streamlit as st 
from data_injection import get_news_link, extract_all_links, formatted_date
from data_injection import news_collection_from_url, save_text_to_file
from data_preprocessing import setup_rag_pipeline
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
groq_api_key = os.environ.get("GROQ_API_KEY")

# Ensure the API key is loaded
if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

### Select News Channel
news_channel = st.sidebar.selectbox("Select News Article Channel.",
                     ["Times Of India", "India Today", "Hindustan News","NDTV", 
                      "Moneycontrol (Stock Market)", "Economic Times (Stock Market)"])

file_path = f"./news collection/{news_channel}/Extracted_news_{formatted_date}.txt"

if news_channel :
    target_url = get_news_link(news_channel)
    news_article_links = extract_all_links(target_url)
    extracted_text = news_collection_from_url(news_article_links)
    save_text_to_file(extracted_text,file_path)


# ## Select Model
llm_model = st.sidebar.selectbox("Select LLM model", ["Maverick","Llama3","Gemma2"])
model_dict = {"Gemma2" : "gemma2-9b-it", "Llama3" : "llama3-8b-8192",
            "Maverick" : "meta-llama/llama-4-maverick-17b-128e-instruct"}
llm = model_dict[llm_model]

#app titles
st.title(f"{news_channel} News Q&A Chatbot by {llm_model}")

# Setup the RAG pipeline and memory
rag_chain, memory = setup_rag_pipeline(file_path, groq_api_key, llm)

# Handle user input
if prompt := st.chat_input("Ask me anything about the news..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = rag_chain.invoke(prompt)
            message_placeholder.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})
            memory.save_context({"input": prompt}, {"output": response})
        except Exception as e:
            message_placeholder.markdown(f"An error occurred: {e}")
            
# Display chat history 
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
