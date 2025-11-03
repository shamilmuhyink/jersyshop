from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sport: Optional[str] = Query(None),
    team: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: Optional[str] = Query("created_at"),
    db: Session = Depends(get_db)
):
    """Get products with optional filtering and pagination"""
    product_service = ProductService(db)
    return await product_service.get_products(
        skip=skip,
        limit=limit,
        sport=sport,
        team=team,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

@router.get("/featured", response_model=List[ProductResponse])
async def get_featured_products(limit: int = Query(8, ge=1, le=20), db: Session = Depends(get_db)):
    """Get featured products"""
    product_service = ProductService(db)
    return await product_service.get_featured_products(limit)

@router.get("/new-arrivals", response_model=List[ProductResponse])
async def get_new_arrivals(limit: int = Query(8, ge=1, le=20), db: Session = Depends(get_db)):
    """Get new arrivals"""
    product_service = ProductService(db)
    return await product_service.get_new_arrivals(limit)

@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search products"""
    product_service = ProductService(db)
    return await product_service.search_products(q, limit)

@router.get("/{slug}", response_model=ProductResponse)
async def get_product(slug: str, db: Session = Depends(get_db)):
    """Get single product by slug"""
    product_service = ProductService(db)
    product = await product_service.get_product_by_slug(slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create new product (admin only)"""
    product_service = ProductService(db)
    return await product_service.create_product(product_data)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update product (admin only)"""
    product_service = ProductService(db)
    product = await product_service.update_product(product_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    """Delete product (admin only)"""
    product_service = ProductService(db)
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/categories/list", response_model=List[str])
async def get_categories(db: Session = Depends(get_db)):
    """Get available sports categories"""
    product_service = ProductService(db)
    return await product_service.get_categories()

@router.get("/teams/list", response_model=List[str])
async def get_teams(sport: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """Get available teams by sport"""
    product_service = ProductService(db)
    return await product_service.get_teams(sport)