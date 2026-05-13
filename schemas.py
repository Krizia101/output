from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ==========================================
# USER SCHEMAS
# ==========================================
class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    full_name: str = Field(..., max_length=100)
    role: str = Field(..., description="admin, coordinator, packaging, production")

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# INGREDIENT & INVENTORY SCHEMAS
# ==========================================
class IngredientBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: Optional[str]
    purchase_unit: str = Field(..., max_length=20)
    usage_unit: str = Field(..., max_length=20)
    conversion_factor: Decimal
    low_stock_threshold: Decimal

class IngredientInDB(IngredientBase):
    id: int
    current_stock_usage: Decimal

    class Config:
        from_attributes = True

class PurchaseCreate(BaseModel):
    ingredient_id: int
    purchase_amount: Decimal
    cost: Decimal
    restock_type: str = Field(default="purchase", description="purchase or harvest")

# ==========================================
# PRODUCT & PRODUCTION SCHEMAS
# ==========================================
class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    price: Decimal = Field(default=150.00)

class ProductInDB(ProductBase):
    id: int
    current_stock_jars: int

    class Config:
        from_attributes = True

class ProductionBatchCreate(BaseModel):
    product_id: int
    jars_produced: int = Field(..., gt=0)

class ProductionBatchInDB(ProductionBatchCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# ORDER SCHEMAS
# ==========================================
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    subtotal: Decimal

class OrderCreate(BaseModel):
    customer_name: str = Field(..., max_length=255)
    payment_method: str = Field(..., max_length=50)
    payment_status: str = Field(default="unpaid")
    items: List[OrderItemBase]

class OrderInDB(BaseModel):
    id: int
    customer_name: str
    total_price: Decimal
    payment_method: str
    payment_status: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True