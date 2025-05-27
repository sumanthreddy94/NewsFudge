# NewsFudge

## Architecture Overview

The system integrates a Streamlit frontend and a FastAPI backend to enable interactive question answering and summarization of current events using Retrieval-Augmented Generation (RAG). The backend leverages OpenAI models, LangChain, and a persistent Chroma vector store.

![Architecture Diagram](/NewsFudge_arch.png)
## Installation & Setup Instructions

### 1.Create and Activate Virtual Environment
```source venv/bin/activate```
```python3 -m venv venv```

### 2.Install Dependencies
```pip install -r requirements.txt```

### 3.Start Server
```uvicorn app.main:app --reload --host 0.0.0.0 --port 8000```

### 4.Streamlit UI
```streamlit run streamlit_app.py --server.port 8502 --server.address 0.0.0.0```