from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ProductResponse, OrderResponse, UserResponse
from app.services.admin_service import AdminService
from app.services.auth_service import get_current_admin_user

router = APIRouter()

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    await get_current_admin_user(db)
    admin_service = AdminService(db)
    return await admin_service.get_dashboard_stats()

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    await get_current_admin_user(db)
    admin_service = AdminService(db)
    return await admin_service.get_users(skip, limit, search, is_active)

@router.get("/orders", response_model=List[OrderResponse])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all orders (admin only)"""
    await get_current_admin_user(db)
    admin_service = AdminService(db)
    return await admin_service.get_orders(skip, limit, status)

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: str,
    tracking_number: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update order status (admin only)"""
    await get_current_admin_user(db)
    admin_service = AdminService(db)
    order = await admin_service.update_order_status(order_id, status, tracking_number)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated successfully"}

@router.get("/analytics")
async def get_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get analytics data (admin only)"""
    await get_current_admin_user(db)
    admin_service = AdminService(db)
    return await admin_service.get_analytics(days)