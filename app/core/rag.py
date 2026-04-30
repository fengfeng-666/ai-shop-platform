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
_all_texts = []  # 保存所有文本，用于重建索引


def add_knowledge(texts: list):
    """添加知识到向量存储。重建整个FAISS索引以保证docstore一致性。"""
    global vector_store, _all_texts
    _all_texts.extend(texts)
    vector_store = FAISS.from_texts(_all_texts, embedding)


def search_knowledge(query: str):
    if vector_store is None:
        return []
    try:
        docs = vector_store.similarity_search(query, k=3)
        return [doc.page_content for doc in docs]
    except Exception:
        return []