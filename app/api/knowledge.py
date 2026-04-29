from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.rag import add_knowledge
from app.core.deps import get_admin_user

router = APIRouter()

class KnowledgeInput(BaseModel):
    texts: list[str]

@router.post("/add")
def add_knowledge_api(data: KnowledgeInput, user=Depends(get_admin_user)):
    add_knowledge(data.texts)
    return {"msg": "知识库添加成功"}