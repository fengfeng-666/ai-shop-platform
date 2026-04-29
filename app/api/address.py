from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.address import Address
from app.core.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 添加地址
@router.post("/add")
def add_address(name: str, phone: str, detail: str,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    addr = Address(
        user_id=user["user_id"],
        name=name,
        phone=phone,
        detail=detail
    )
    db.add(addr)
    db.commit()
    return {"msg": "添加成功"}

# 获取地址列表
@router.get("/")
def get_address(db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    return db.query(Address).filter(
        Address.user_id == user["user_id"]
    ).all()