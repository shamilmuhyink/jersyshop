from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class CartItemBase(BaseModel):
    product_id: UUID
    product_variant_id: UUID
    quantity: int = Field(..., gt=0, le=10)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, le=10)

class CartItemResponse(CartItemBase):
    id: UUID
    added_at: datetime

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: Decimal
    item_count: int

    class Config:
        from_attributes = True