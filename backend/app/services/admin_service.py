from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from app.models.user import User
from app.models.order import Order
from app.models.product import Product

class AdminService:
    def __init__(self, db: Session):
        self.db = db

    async def get_dashboard_stats(self) -> dict:
        # Get basic stats
        total_users = self.db.query(User).filter(User.is_active == True).count()
        total_orders = self.db.query(Order).count()
        total_products = self.db.query(Product).filter(Product.is_active == True).count()

        # Get revenue stats
        total_revenue = (
            self.db.query(func.sum(Order.total_amount))
            .filter(Order.status.in_(['delivered', 'shipped']))
            .scalar() or Decimal('0')
        )

        # Get recent orders count (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_orders = (
            self.db.query(Order)
            .filter(Order.created_at >= seven_days_ago)
            .count()
        )

        # Get low stock products
        low_stock_products = (
            self.db.query(Product)
            .join(Product.variants)
            .filter(ProductVariant.stock_quantity < 5)
            .distinct()
            .count()
        )

        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_revenue": float(total_revenue),
            "recent_orders": recent_orders,
            "low_stock_products": low_stock_products,
        }

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        query = self.db.query(User)

        if search:
            query = query.filter(
                or_(
                    User.first_name.ilike(f"%{search}%"),
                    User.last_name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%")
                )
            )

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        return query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()

    async def get_orders(
        self,
        skip: int = 0,
        limit: int = 50,
        status_filter: Optional[str] = None
    ) -> List[Order]:
        query = self.db.query(Order)

        if status_filter:
            try:
                from app.models.order import OrderStatus
                status_enum = OrderStatus(status_filter)
                query = query.filter(Order.status == status_enum)
            except ValueError:
                pass

        return query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()

    async def update_order_status(
        self,
        order_id: str,
        status: str,
        tracking_number: Optional[str] = None
    ) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None

        try:
            from app.models.order import OrderStatus
            order.status = OrderStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status"
            )

        if tracking_number:
            order.tracking_number = tracking_number

        self.db.commit()
        self.db.refresh(order)
        return order

    async def get_analytics(self, days: int = 30) -> dict:
        start_date = datetime.utcnow() - timedelta(days=days)

        # Revenue over time
        revenue_by_day = (
            self.db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total_amount).label('revenue'),
                func.count(Order.id).label('orders')
            )
            .filter(Order.created_at >= start_date)
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
            .all()
        )

        # Top selling products
        top_products = (
            self.db.query(
                Product.name,
                func.sum(OrderItem.quantity).label('total_sold')
            )
            .join(OrderItem)
            .join(Order)
            .filter(Order.created_at >= start_date)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(10)
            .all()
        )

        # Orders by status
        orders_by_status = (
            self.db.query(
                Order.status,
                func.count(Order.id).label('count')
            )
            .filter(Order.created_at >= start_date)
            .group_by(Order.status)
            .all()
        )

        return {
            "revenue_by_day": [
                {
                    "date": str(item.date),
                    "revenue": float(item.revenue),
                    "orders": item.orders
                }
                for item in revenue_by_day
            ],
            "top_products": [
                {
                    "name": item.name,
                    "total_sold": item.total_sold
                }
                for item in top_products
            ],
            "orders_by_status": [
                {
                    "status": item.status.value if hasattr(item.status, 'value') else str(item.status),
                    "count": item.count
                }
                for item in orders_by_status
            ]
        }