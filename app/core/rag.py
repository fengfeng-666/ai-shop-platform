from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_BASE_URL"),
    model="text-embedding-v3"  # 通义千问的embedding模型
)

vector_store = None

def add_knowledge(texts: list):
    global vector_store
    if vector_store is None:
        vector_store = FAISS.from_texts(texts, embedding)
    else:
        vector_store.add_texts(texts)

def search_knowledge(query: str):
    if vector_store is None:
        return []
    docs = vector_store.similarity_search(query, k=3)
    return [doc.page_content for doc in docs]