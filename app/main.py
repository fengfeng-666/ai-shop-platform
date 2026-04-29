from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import user,product,cart,order,ai,knowledge,recommend,address

app = FastAPI()

# 创建表
Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(user.router, prefix="/user")
app.include_router(product.router, prefix="/product", tags=["商品"])
app.include_router(cart.router, prefix="/cart", tags=["购物车"])
app.include_router(order.router, prefix="/order", tags=["订单"])
app.include_router(ai.router, prefix="/ai", tags=["AI助手"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["知识库"])
app.include_router(recommend.router, prefix="/recommend", tags=["推荐"])
app.include_router(address.router, prefix="/address", tags=["地址"])


@app.get("/")
def root():
    return {"msg": "API running"}