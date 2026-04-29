from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.address import Address
from app.core.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_order(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == user["user_id"]).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="购物车为空")

    total_price = 0
    order = Order(user_id=user["user_id"], total_price=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        total_price += product.price * item.quantity
        db.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        ))
    order.total_price = total_price

    # 清空购物车
    db.query(Cart).filter(Cart.user_id == user["user_id"]).delete()
    db.commit()

    return {"msg": "下单成功", "total_price": total_price}


@router.post("/pay")
def pay_order(address_id: int,
              db: Session = Depends(get_db),
              user=Depends(get_current_user)):

    cart_items = db.query(Cart).filter(Cart.user_id == user["user_id"]).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="购物车为空")

    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    if address.user_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="无权使用该地址")

    total_price = 0
    order = Order(user_id=user["user_id"], total_price=0, status="paid")
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            total_price += product.price * item.quantity
            db.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            ))
    order.total_price = total_price

    db.query(Cart).filter(Cart.user_id == user["user_id"]).delete()
    db.commit()

    return {"msg": "支付成功", "order_id": order.id, "total_price": total_price}


@router.get("/list")
def order_list(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user["user_id"]).all()
    return [
        {
            "id": o.id,
            "price": o.total_price,
            "status": o.status
        }
        for o in orders
    ]