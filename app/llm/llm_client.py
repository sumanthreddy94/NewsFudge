from langchain.chat_models.openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

from app.api.services.embeddings import get_retriever

def get_llm():
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.2)
    return llm

def get_retrieval_chain():
    prompt_template = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        llm = get_llm(),
        prompt= prompt_template
        )
    
    retrieval_chain = create_retrieval_chain(
        retriever = get_retriever(),
        combine_docs_chain = combine_docs_chain
    )
    return retrieval_chain
