from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    total_price = Column(Float)
    status = Column(String(20), default="pending")  # pending / paid