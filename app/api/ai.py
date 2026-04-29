# app/api/ai.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.ai import chat_with_qwen
from app.core.deps import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_ai(data: ChatRequest, user=Depends(get_current_user)):
    """
    需要登录后才能使用AI助手，工具会根据当前用户操作
    """
    reply = chat_with_qwen(data.message, user_id=user.get("user_id"))
    return {"reply": reply}