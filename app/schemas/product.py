from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    description: str

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str
    description: str

    model_config = ConfigDict(from_attributes=True)  # 代替旧版 orm_mode