import json
from app.db.db_client import get_persist_chroma
from langchain.vectorstores import Chroma

from app.models.conversations import QA, Conversation

chroma_client = get_persist_chroma()
collection = chroma_client.get_or_create_collection(name="conversations")


async def add_conversation(conversation: Conversation):
    collection.add(
    documents=[conversation.model_dump_json()],
    ids=[conversation.id],
    metadatas=[{"title": conversation.title, "created_at": conversation.created_at.isoformat()}]
)
    
async def get_conversation_by_id(convo_id):
    result = collection.get(ids=[convo_id], include=["documents"])
    if result["documents"]:
        document_str = result["documents"][0]
        document_dict = json.loads(document_str)
        return Conversation(**document_dict)
    return None

async def update_conversation(convo_id: str, new_qa: QA):
    convo = await get_conversation_by_id(convo_id)
    if not convo:
        return None
    convo.qa_list.append(new_qa)
    # Delete old and re-add
    collection.delete(ids=[convo_id])
    collection.add(
        documents=[convo.model_dump_json()],
        ids=[convo_id],
        metadatas=[{"title": convo.title, "created_at": convo.created_at.isoformat()}]
    )
    return convo

async def get_all_conversations():
    results = collection.get(include=["documents"])
    conversations = [json.loads(doc) for doc in results["documents"]]
    return conversations