from sqlalchemy import Column, Integer, String
from app.db.database import Base

class UserBehavior(Base):
    __tablename__ = "user_behavior"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    action = Column(String(50))  # view / search
    content = Column(String(100))  # 关键词