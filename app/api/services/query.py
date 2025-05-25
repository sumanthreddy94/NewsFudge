from app.api.services.embeddings import get_embedding_model
from app.core.config import QA_COLLECTION_NAME
from app.db.db_client import get_in_mem_chroma
from app.llm.llm_client import get_retrieval_chain
from app.models.news_dataset import SearchResultItem

embedding_model = get_embedding_model()
chroma_client = get_in_mem_chroma()
collection = chroma_client.create_collection(name=QA_COLLECTION_NAME)

# Gets Only Raw Matching Data
async def search_chroma(query: str, top_k: int = 3):

    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    result_items = []

    for i, doc in enumerate(results['documents'][0]):
        snippet = doc[:200] + "..." if len(doc) > 200 else doc
        metadata = results['metadatas'][0][i]
        result_items.append(SearchResultItem(
            text_snippet=snippet,
            title=metadata.get('title'),
            url=metadata.get('url'),
        ))

    result_items

async def get_by_query(query: str):
    retrieval_chain = get_retrieval_chain()
    result = await retrieval_chain.ainvoke({"input": query})
    
    return result



