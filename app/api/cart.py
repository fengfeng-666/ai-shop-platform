from fastapi import APIRouter, Depends, HTTPException
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
    if quantity < 1:
        raise HTTPException(status_code=400, detail="数量必须大于0")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    existing = db.query(Cart).filter(
        Cart.user_id == user["user_id"],
        Cart.product_id == product_id
    ).first()

    if existing:
        existing.quantity += quantity
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="加入购物车失败")
        return {"msg": "已更新购物车数量"}

    cart = Cart(
        user_id=user["user_id"],
        product_id=product_id,
        quantity=quantity
    )
    db.add(cart)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="加入购物车失败")
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
    if quantity < 1:
        raise HTTPException(status_code=400, detail="数量必须大于0")

    cart = db.query(Cart).filter(
        Cart.user_id == user["user_id"],
        Cart.product_id == product_id
    ).first()

    if not cart:
        raise HTTPException(status_code=404, detail="商品不在购物车")

    cart.quantity = quantity
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="更新失败")

    return {"msg": "更新成功"}

@router.delete("/delete")
def delete_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = db.query(Cart).filter(
        Cart.user_id == user["user_id"],
        Cart.product_id == product_id
    ).delete()

    if result == 0:
        raise HTTPException(status_code=404, detail="商品不在购物车")

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="删除失败")
    return {"msg": "删除成功"}

@router.get("/detail")
def cart_detail(db: Session = Depends(get_db), user=Depends(get_current_user)):
    carts = db.query(Cart).filter(
        Cart.user_id == user["user_id"]
    ).all()

    if not carts:
        return {"items": [], "total_price": 0}

    product_ids = [c.product_id for c in carts]
    products = {
        p.id: p
        for p in db.query(Product).filter(Product.id.in_(product_ids)).all()
    }

    result = []
    total_price = 0

    for c in carts:
        product = products.get(c.product_id)
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
