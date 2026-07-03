from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.core.deps import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    if len(user.username.strip()) < 2:
        raise HTTPException(status_code=400, detail="用户名至少2个字符")
    db_user = User(
        username=user.username.strip(),
        password=hash_password(user.password)
    )
    db.add(db_user)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="注册失败")
    return {"msg": "注册成功"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })
    return {
        "msg": "登录成功!",
        "access_token": token,
        "token_type": "bearer"
    }

# 修改用户名
@router.put("/update")
def update_username(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 检查新用户名是否已被占用
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已被使用")

    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db_user.username = username
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="修改失败")
    return {"msg": "用户名修改成功"}

# 修改密码
@router.put("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if not verify_password(old_password, db_user.password):
        raise HTTPException(status_code=400, detail="当前密码错误")

    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码长度不能少于6位")

    db_user.password = hash_password(new_password)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="修改失败")
    return {"msg": "密码修改成功"}