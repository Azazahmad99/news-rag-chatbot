# 📰 News RAG Chatbot (India Edition)

An intelligent chatbot that scrapes the latest news articles from top Indian media outlets and enables question answering through a powerful Retrieval-Augmented Generation (RAG) pipeline using **Groq's LLaMA3 / Gemma2 models**.

Built using **Streamlit**, **BeautifulSoup**, **LangChain**, and **Groq API**.

---

## 🚀 Features

- 🔍 Scrape news from:
  - Times of India
  - India Today
  - Hindustan Times
  - NDTV
  - Moneycontrol (Stock Market)
  - Economic Times (Stock Market)

- 🧠 Retrieval-Augmented Generation (RAG) pipeline:
  - Text extraction from real news sources
  - Vectorization via HuggingFace embeddings
  - ChromaDB for retrieval
  - Groq LLM for answer generation (LLaMA3 / Gemma2)

- 💬 Streamlit-based Chat UI
- 🗂️ Save news data with timestamps for offline reference

---

## 🛠️ Tech Stack

| Component       | Tool/Library                       |
|----------------|------------------------------------|
| Frontend       | Streamlit                          |
| Scraping       | BeautifulSoup, Requests            |
| RAG Pipeline   | LangChain, HuggingFace, ChromaDB   |
| LLM Backend    | Groq API (LLaMA3 / Gemma2)         |
| Environment    | Python, dotenv                     |

---

## 📁 Project Structure

📦 news-rag-chatbot/
├── data_injection.py
├── data_preprocessing.py
├── main_app.py
├── .env
├── requirements.txt
├── README.md
└── news collection/

----------------------------------------------------------

## Installation Steps

1. Clone the repository
```bash
git clone https://github.com/your-username/news-rag-chatbot.git
cd news-rag-chatbot
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
GROQ_API_KEY="your_groq_api_key"

▶️ Run the App
```bash
streamlit run main_app.py
```

Choose a news channel from the sidebar, select your preferred LLM (Gemma2 or LLaMA3), and start chatting with the news!
