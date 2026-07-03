from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
import os
import logging
import requests
import threading
from typing import List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DASHSCOPE_EMBEDDING_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"
DASHSCOPE_API_KEY = os.getenv("OPENAI_API_KEY")


class DashScopeEmbeddings(Embeddings):
    """通义千问原生 Embedding API 封装，绕过兼容模式的格式转换问题。"""

    def __init__(self, api_key: str, model: str = "text-embedding-v2"):
        self.api_key = api_key
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        resp = requests.post(
            DASHSCOPE_EMBEDDING_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "input": {"texts": texts}},
            timeout=30,
        )
        data = resp.json()
        if resp.status_code != 200:
            raise RuntimeError(f"Embedding API 调用失败: {data}")
        return [e["embedding"] for e in data["output"]["embeddings"]]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


embedding = DashScopeEmbeddings(api_key=DASHSCOPE_API_KEY)

vector_store = None
_all_texts = []
_lock = threading.Lock()


def add_knowledge(texts: list):
    global vector_store, _all_texts
    with _lock:
        _all_texts.extend(texts)
        vector_store = FAISS.from_texts(_all_texts, embedding)


def search_knowledge(query: str):
    with _lock:
        if vector_store is None:
            return []
        try:
            docs = vector_store.similarity_search(query, k=3)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.warning(f"知识库搜索失败: {e}")
            return []