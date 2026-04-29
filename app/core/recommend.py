from app.db.database import SessionLocal
from app.models.user_behavior import UserBehavior
from app.models.product import Product

def recommend_products(user_id: int):
    db = SessionLocal()

    # 获取最近行为
    behaviors = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id
    ).all()

    keywords = [b.content for b in behaviors]

    # 简单策略：取最后一个关键词
    if not keywords:
        return db.query(Product).limit(5).all()

    keyword = keywords[-1]

    products = db.query(Product).filter(
        Product.name.contains(keyword)
    ).limit(5).all()

    db.close()
    return products