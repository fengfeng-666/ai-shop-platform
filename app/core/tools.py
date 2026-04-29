# app/core/tools.py
from app.db.database import SessionLocal
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


def find_product(keyword: str, max_price: float = None):
    db = SessionLocal()
    try:
        query = db.query(Product).filter(Product.name.contains(keyword))
        if max_price:
            query = query.filter(Product.price <= max_price)
        product = query.first()
        if not product:
            return "未找到相关商品"
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
    finally:
        db.close()

def add_to_cart_tool(user_id: int, product_id: int, quantity: int = 1):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return "商品不存在"
        cart = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart)
        db.commit()
        return f"已将 {product.name} x{quantity} 加入购物车"
    except Exception as e:
        db.rollback()
        return f"加入购物车失败：{str(e)}"
    finally:
        db.close()

def auto_order_tool(user_id: int, address_id: int):
    db = SessionLocal()
    try:
        cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
        if not cart_items:
            return "购物车为空"

        total_price = 0
        order = Order(user_id=user_id, total_price=0, status="paid")
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
        db.query(Cart).filter(Cart.user_id == user_id).delete()
        db.commit()

        return f"下单成功，总价{total_price}元，订单ID：{order.id}"
    except Exception as e:
        db.rollback()
        return f"下单失败：{str(e)}"
    finally:
        db.close()