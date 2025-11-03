from sqlalchemy import Column, String, Boolean, DateTime, Text, Numeric, Integer, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    team = Column(String(100), nullable=False, index=True)
    player = Column(String(100))
    sport = Column(String(50), nullable=False, index=True)
    brand = Column(String(50))
    base_price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2))
    material = Column(String(100))
    care_instructions = Column(Text)
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    variants = relationship("ProductVariant", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    size = Column(String(10), nullable=False)
    color = Column(String(50))
    sku = Column(String(50), unique=True, nullable=False, index=True)
    stock_quantity = Column(Integer, default=0)
    price = Column(Numeric(10, 2))
    image_urls = Column(JSON, default=list)

    # Relationships
    product = relationship("Product", back_populates="variants")
    order_items = relationship("OrderItem", back_populates="variant")
    cart_items = relationship("CartItem", back_populates="variant")