from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.cart import Cart
from app.core.deps import get_current_user
from app.models.product import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ➕ 加入购物车
@router.post("/add")
def add_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart = Cart(
        user_id=user["user_id"],
        product_id=product_id,
        quantity=quantity
    )
    db.add(cart)
    db.commit()
    return {"msg": "加入购物车成功"}

# 📋 查看购物车
@router.get("/")
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Cart).filter(Cart.user_id == user["user_id"]).all()

@router.put("/update")
def update_cart(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.user_id == user["user_id"],
        Cart.product_id == product_id
    ).first()

    if not cart:
        return {"msg": "商品不在购物车"}

    cart.quantity = quantity
    db.commit()

    return {"msg": "更新成功"}

@router.delete("/delete")
def delete_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db.query(Cart).filter(
        Cart.user_id == user["user_id"],
        Cart.product_id == product_id
    ).delete()

    db.commit()
    return {"msg": "删除成功"}

@router.get("/detail")
def cart_detail(db: Session = Depends(get_db), user=Depends(get_current_user)):
    carts = db.query(Cart).filter(
        Cart.user_id == user["user_id"]
    ).all()

    result = []
    total_price = 0

    for c in carts:
        product = db.query(Product).filter(Product.id == c.product_id).first()

        if not product:
            continue

        subtotal = product.price * c.quantity
        total_price += subtotal

        result.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": c.quantity,
            "subtotal": subtotal
        })

    return {
        "items": result,
        "total_price": total_price
    }
