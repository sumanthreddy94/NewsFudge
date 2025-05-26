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

# import json
# from app.db.db_client import get_persist_chroma
# from langchain.vectorstores import Chroma

# from app.models.conversations import QA, Conversation

# chroma_client = get_persist_chroma()
# collection = chroma_client.get_or_create_collection(name="conversations")


# async def add_conversation(conversation: Conversation):
#     doc_json = conversation.model_dump_json()
#     print(f"[ADD] Adding conversation ID={conversation.id}")
#     print(f"[ADD] Payload to Chroma (document): {doc_json}")
#     print(f"[ADD] Metadata: {{'title': {conversation.title}, 'created_at': {conversation.created_at.isoformat()}}}")
    
#     collection.add(
#         documents=[doc_json],
#         ids=[conversation.id],
#         metadatas=[{"title": conversation.title, "created_at": conversation.created_at.isoformat()}]
#     )


# async def get_conversation_by_id(convo_id):
#     # print(f"[GET] Retrieving conversation ID={convo_id}")
#     result = collection.get(ids=[convo_id], include=["documents"])
#     # print(f"[GET] Raw result from Chroma: {result}")
    
#     if result["documents"]:
#         document_str = result["documents"][0]
#         # print(f"[GET] Retrieved document string: {document_str}")
        
#         document_dict = json.loads(document_str)
#         # print(f"[GET] Parsed document as dict: {document_dict}")
        
#         return Conversation(**document_dict)
    
#     # print(f"[GET] No conversation found with ID={convo_id}")
#     return None


# async def update_conversation(convo_id: str, new_qa: QA):
#     # print(f"[UPDATE] Updating conversation ID={convo_id} with new QA: {new_qa}")
    
#     convo = await get_conversation_by_id(convo_id)
#     if not convo:
#         print(f"[UPDATE] No conversation found with ID={convo_id}. Cannot update.")
#         return None
    
#     convo.qa_list.append(new_qa)
#     print(f"[UPDATE] Updated QA list: {convo.qa_list}")

#     collection.delete(ids=[convo_id])
#     print(f"[UPDATE] Deleted old document with ID={convo_id} from Chroma")

#     doc_json = convo.model_dump_json()
#     print(f"[UPDATE] New document JSON: {doc_json}")
    
#     collection.add(
#         documents=[doc_json],
#         ids=[convo_id],
#         metadatas=[{"title": convo.title, "created_at": convo.created_at.isoformat()}]
#     )
    
#     return convo


# async def get_all_conversations():
#     print(f"[GET_ALL] Fetching all conversations from Chroma")
#     results = collection.get(include=["documents"])
#     print(f"[GET_ALL] Raw result: {results}")
    
#     conversations = []
#     for doc in results["documents"]:
#         try:
#             parsed = json.loads(doc)
#             print(f"[GET_ALL] Parsed conversation: {parsed}")
#             conversations.append(parsed)
#         except json.JSONDecodeError as e:
#             print(f"[GET_ALL] Failed to parse document: {doc}")
#             print(f"[GET_ALL] Error: {e}")
    
#     return conversations
