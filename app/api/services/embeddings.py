import datetime
from app.api.services.data_cleaning import prepare_documents_for_embedding, load_and_clean_all
from app.core.config import HISTORY_COLLECTION_NAME, QA_COLLECTION_NAME
from app.db.db_client import get_in_mem_chroma, get_persist_chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

from app.models.news_dataset import CleanedArticle
from itertools import islice

chroma_client = get_persist_chroma()

def get_Vectorstore(collection_name: str):
    vector_store = Chroma(
        collection_name = collection_name,
        embedding_function = get_embedding_model(),
        client = chroma_client
    )
    return vector_store


def get_embedding_model(model_name="all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)

def batch_iterable(iterable, batch_size):
    """Yield successive batches from iterable."""
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch

MAX_CHROMA_BATCH_SIZE = 40000  # slightly below limit

def embed_articles(cleaned_articles: list[CleanedArticle]):
    documents, metadatas, ids = prepare_documents_for_embedding(cleaned_articles)
    if not documents:
        print("No valid articles to embed.")
        return

    vector_store = get_Vectorstore(QA_COLLECTION_NAME)

    docs = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(documents, metadatas)
    ]

    # Batch to stay under ChromaDB limit
    for doc_batch in batch_iterable(docs, MAX_CHROMA_BATCH_SIZE):
        vector_store.add_documents(doc_batch)

    print(f"Embedded and stored {len(documents)} articles in Chroma via vector_store.")

def get_retriever():
    qa_vactorstore = get_Vectorstore(QA_COLLECTION_NAME)
    retriever = qa_vactorstore.as_retriever(search_kwargs={"k": 5}, return_source_documents=True)

    return retriever

def embed_history(conversation_id: str, question: str, answer: str):
    doc_text = f"Q: {question}\nA: {answer}"
    metadata = {
        "conversation_id": conversation_id,
        "timestamp": datetime.utcnow().isoformat(),
    }

    history_vectorstore = get_Vectorstore(HISTORY_COLLECTION_NAME)
    doc = Document(page_content=doc_text, metadata=metadata)
    history_vectorstore.add_documents([doc])
    print(f"Stored Q&A history in Chroma for conversation_id={conversation_id}")