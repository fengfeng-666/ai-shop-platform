from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.core.recommend import recommend_products
from app.db.database import SessionLocal
from app.models.product import Product
from app.models.user_behavior import UserBehavior

router = APIRouter()

@router.get("/")
def recommend_products(user_id: int):
    db = SessionLocal()
    try:
        behaviors = db.query(UserBehavior).filter(UserBehavior.user_id == user_id).all()
        keywords = [b.content for b in behaviors]
        if not keywords:
            return db.query(Product).limit(5).all()
        keyword = keywords[-1]
        return db.query(Product).filter(Product.name.contains(keyword)).limit(5).all()
    finally:
        db.close()
