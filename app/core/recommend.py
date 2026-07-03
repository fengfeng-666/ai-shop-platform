from app.db.database import SessionLocal
from app.models.user_behavior import UserBehavior
from app.models.product import Product

def recommend_products(user_id: int):
    db = SessionLocal()
    try:
        behaviors = db.query(UserBehavior).filter(
            UserBehavior.user_id == user_id
        ).all()

        keywords = [b.content for b in behaviors]

        if not keywords:
            return db.query(Product).limit(5).all()

        keyword = keywords[-1]
        products = db.query(Product).filter(
            Product.name.contains(keyword)
        ).limit(5).all()

        return products
    finally:
        db.close()