import chromadb
from chromadb.config import Settings

def get_in_mem_chroma():
    chroma_client = chromadb.EphemeralClient()
    return chroma_client

def get_persist_chroma():
    chroma_client = chromadb.PersistentClient(path="/Users/sumanthanumula/Downloads/chromadb_data")
    return chroma_client