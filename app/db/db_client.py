import chromadb
from chromadb.config import Settings

def get_in_mem_chroma():
    chroma_client = chromadb.EphemeralClient()
    return chroma_client