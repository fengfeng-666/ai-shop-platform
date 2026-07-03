from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.core.rag import add_knowledge
from app.core.deps import get_admin_user

router = APIRouter()


class KnowledgeInput(BaseModel):
    texts: list[str] = Field(max_length=100)


@router.post("/add")
def add_knowledge_api(data: KnowledgeInput, user=Depends(get_admin_user)):
    if not data.texts:
        raise HTTPException(status_code=400, detail="知识内容不能为空")
    if len(data.texts) > 100:
        raise HTTPException(status_code=400, detail="最多添加100条知识")
    try:
        add_knowledge(data.texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识库添加失败: {e}")
    return {"msg": f"知识库添加成功，共 {len(data.texts)} 条"}