from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
async def get_user_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get current user's orders"""
    current_user = await get_current_user(db)
    order_service = OrderService(db)
    return await order_service.get_user_orders(current_user.id, skip, limit, status)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get specific order details"""
    current_user = await get_current_user(db)
    order_service = OrderService(db)
    order = await order_service.get_order(order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create new order"""
    current_user = await get_current_user(db)
    order_service = OrderService(db)
    return await order_service.create_order(order_data, current_user.id)

@router.post("/{order_id}/cancel")
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    """Cancel order"""
    current_user = await get_current_user(db)
    order_service = OrderService(db)
    success = await order_service.cancel_order(order_id, current_user.id)
    if not success:
        raise HTTPException(status_code=400, detail="Order cannot be cancelled")
    return {"message": "Order cancelled successfully"}