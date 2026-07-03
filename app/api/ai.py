# app/api/ai.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.core.ai import chat_with_qwen
from app.core.deps import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

@router.post("/chat")
def chat_ai(data: ChatRequest, user=Depends(get_current_user)):
    """
    需要登录后才能使用AI助手，工具会根据当前用户操作
    """
    reply = chat_with_qwen(data.message, user_id=user.get("user_id"))
    return {"reply": reply}