from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from sqlalchemy import or_
from app.core.deps import get_admin_user
from app.core.deps import get_current_user
from app.models.user_behavior import UserBehavior

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ 添加商品（管理员用）
@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_admin_user)  # 👈 加这一行
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# 📋 商品列表
@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# 🔍 搜索商品
@router.get("/search")
def search_products(
    keyword: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 记录行为
    behavior = UserBehavior(
        user_id=user["user_id"],
        action="search",
        content=keyword
    )
    db.add(behavior)
    db.commit()

    return db.query(Product).filter(
        Product.name.contains(keyword)
    ).all()