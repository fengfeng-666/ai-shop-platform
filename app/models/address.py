from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50))        # 收件人
    phone = Column(String(20))
    detail = Column(String(200))     # 地址