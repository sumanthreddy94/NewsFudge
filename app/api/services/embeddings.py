from app.api.services.data_cleaning import prepare_documents_for_embedding, load_and_clean_all
from app.db.db_client import get_in_mem_chroma
from langchain.embeddings import HuggingFaceEmbeddings

from app.models.news_dataset import CleanedArticle
from itertools import islice

chroma_client = get_in_mem_chroma()
collection = chroma_client.create_collection(name="news_articles")


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

def embed_articles(cleaned_articles: list[CleanedArticle]):
    documents, metadatas, ids = prepare_documents_for_embedding(cleaned_articles)
    if not documents:
        print("No valid articles to embed.")
        return
    embedding_model = get_embedding_model()
    embeddings = embedding_model.embed_documents(documents)

    max_batch_size = 40000  # stay under ChromaDB limit (41666)

    for doc_batch, meta_batch, id_batch, emb_batch in zip(
        batch_iterable(documents, max_batch_size),
        batch_iterable(metadatas, max_batch_size),
        batch_iterable(ids, max_batch_size),
        batch_iterable(embeddings, max_batch_size),
    ):
        collection.add(
            documents=doc_batch,
            metadatas=meta_batch,
            ids=id_batch,
            embeddings=emb_batch,
        )
    print(f"Embedded and stored {len(documents)} articles in Chroma.")