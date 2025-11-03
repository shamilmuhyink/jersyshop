from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    team: str = Field(..., min_length=1, max_length=100)
    player: Optional[str] = Field(None, max_length=100)
    sport: str = Field(..., min_length=1, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    base_price: Decimal = Field(..., gt=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    material: Optional[str] = Field(None, max_length=100)
    care_instructions: Optional[str] = None

class ProductCreate(ProductBase):
    slug: str
    variants: List['ProductVariantCreate']

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    team: Optional[str] = Field(None, min_length=1, max_length=100)
    player: Optional[str] = Field(None, max_length=100)
    sport: Optional[str] = Field(None, min_length=1, max_length=50)
    brand: Optional[str] = Field(None, max_length=50)
    base_price: Optional[Decimal] = Field(None, gt=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    material: Optional[str] = Field(None, max_length=100)
    care_instructions: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: UUID
    slug: str
    average_rating: Optional[float] = 0.0
    review_count: int = 0
    is_active: bool
    created_at: datetime
    updated_at: datetime
    variants: List['ProductVariantResponse']

    class Config:
        from_attributes = True

class ProductVariantBase(BaseModel):
    size: str = Field(..., min_length=1, max_length=10)
    color: Optional[str] = Field(None, max_length=50)
    sku: str = Field(..., min_length=1, max_length=50)
    stock_quantity: int = Field(..., ge=0)
    price: Optional[Decimal] = Field(None, ge=0)
    image_urls: List[str] = []

class ProductVariantCreate(ProductVariantBase):
    product_id: UUID

class ProductVariantResponse(ProductVariantBase):
    id: UUID
    product_id: UUID

    class Config:
        from_attributes = True

# Forward reference resolution
ProductCreate.model_rebuild()
ProductResponse.model_rebuild()