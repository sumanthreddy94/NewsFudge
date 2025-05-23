from app.api.services.data_cleaning import prepare_documents_for_embedding, load_and_clean_all
from app.db.db_client import get_in_mem_chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

from app.models.news_dataset import CleanedArticle
from itertools import islice

chroma_client = get_in_mem_chroma()
# collection = chroma_client.get_or_create_collection(name="news_articles")
def get_Vectorstore():
    vector_store = Chroma(
        collection_name = "news_articles",
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

# def embed_articles(cleaned_articles: list[CleanedArticle]):
#     documents, metadatas, ids = prepare_documents_for_embedding(cleaned_articles)
#     if not documents:
#         print("No valid articles to embed.")
#         return
#     embedding_model = get_embedding_model()
#     embeddings = embedding_model.embed_documents(documents)

#     max_batch_size = 40000  # stay under ChromaDB limit (41666)
#     vectore_store = get_Vectorstore()

#     for doc_batch, meta_batch, id_batch, emb_batch in zip(
#         batch_iterable(documents, max_batch_size),
#         batch_iterable(metadatas, max_batch_size),
#         batch_iterable(ids, max_batch_size),
#         batch_iterable(embeddings, max_batch_size),
#     ):
#         collection.add(
#             documents=doc_batch,
#             metadatas=meta_batch,
#             ids=id_batch,
#             embeddings=emb_batch,
#         )
#     print(f"Embedded and stored {len(documents)} articles in Chroma.")

MAX_CHROMA_BATCH_SIZE = 40000  # slightly below limit

def embed_articles(cleaned_articles: list[CleanedArticle]):
    documents, metadatas, ids = prepare_documents_for_embedding(cleaned_articles)
    if not documents:
        print("No valid articles to embed.")
        return

    vector_store = get_Vectorstore()

    docs = [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(documents, metadatas)
    ]

    # Batch to stay under ChromaDB limit
    for doc_batch in batch_iterable(docs, MAX_CHROMA_BATCH_SIZE):
        vector_store.add_documents(doc_batch)

    print(f"Embedded and stored {len(documents)} articles in Chroma via vector_store.")

def get_retriever():
    retriever = Chroma(
        collection_name = "news_articles",
        embedding_function = get_embedding_model(),
        client = chroma_client
    ).as_retriever(search_kwargs={"k": 5}, return_source_documents=True)

    return retriever

