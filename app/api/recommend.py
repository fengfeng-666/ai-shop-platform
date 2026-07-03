from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.db.database import SessionLocal
from app.models.product import Product
from app.models.user_behavior import UserBehavior

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_recommend_products(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    behaviors = db.query(UserBehavior).filter(UserBehavior.user_id == user["user_id"]).all()
    keywords = [b.content for b in behaviors]
    if not keywords:
        return db.query(Product).limit(5).all()
    keyword = keywords[-1]
    return db.query(Product).filter(Product.name.contains(keyword)).limit(5).all()
