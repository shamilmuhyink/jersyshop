from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import uuid
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import ProductVariant
from app.schemas import OrderCreate

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def generate_order_number(self) -> str:
        return f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    async def get_user_orders(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[str] = None
    ) -> List[Order]:
        query = self.db.query(Order).filter(Order.user_id == user_id)

        if status_filter:
            try:
                status_enum = OrderStatus(status_filter)
                query = query.filter(Order.status == status_enum)
            except ValueError:
                pass  # Invalid status, ignore filter

        return query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()

    async def get_order(self, order_id: str, user_id: str) -> Optional[Order]:
        return (
            self.db.query(Order)
            .filter(and_(Order.id == order_id, Order.user_id == user_id))
            .first()
        )

    async def create_order(self, order_data: OrderCreate, user_id: str) -> Order:
        # Validate stock and calculate totals
        subtotal = Decimal('0')
        order_items = []

        for item in order_data.items:
            # Get product variant
            variant = (
                self.db.query(ProductVariant)
                .filter(ProductVariant.id == item.product_variant_id)
                .first()
            )

            if not variant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product variant {item.product_variant_id} not found"
                )

            if variant.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {variant.size}"
                )

            # Calculate price
            unit_price = variant.price or variant.product.base_price
            if variant.product.sale_price:
                unit_price = variant.product.sale_price

            item_total = unit_price * item.quantity
            subtotal += item_total

            order_items.append({
                "product_variant": variant,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "total_price": item_total
            })

        # Calculate totals
        tax_amount = subtotal * Decimal('0.08')  # 8% tax
        shipping_amount = Decimal('9.99')
        if subtotal >= Decimal('100'):
            shipping_amount = Decimal('0')  # Free shipping over $100

        total_amount = subtotal + tax_amount + shipping_amount

        # Create order
        db_order = Order(
            user_id=user_id,
            order_number=self.generate_order_number(),
            subtotal=subtotal,
            tax_amount=tax_amount,
            shipping_amount=shipping_amount,
            total_amount=total_amount,
            shipping_address=order_data.shipping_address.dict(),
            billing_address=order_data.billing_address.dict() if order_data.billing_address else None,
            payment_method=order_data.payment_method,
            notes=order_data.notes,
        )

        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)

        # Create order items and update stock
        for item_data in order_items:
            # Create order item
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=item_data["product_variant"].product_id,
                product_variant_id=item_data["product_variant"].id,
                product_name=item_data["product_variant"].product.name,
                product_image=item_data["product_variant"].image_urls[0] if item_data["product_variant"].image_urls else None,
                size=item_data["product_variant"].size,
                color=item_data["product_variant"].color,
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["total_price"],
            )
            self.db.add(order_item)

            # Update stock
            item_data["product_variant"].stock_quantity -= item_data["quantity"]

        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    async def cancel_order(self, order_id: str, user_id: str) -> bool:
        order = (
            self.db.query(Order)
            .filter(and_(Order.id == order_id, Order.user_id == user_id))
            .first()
        )

        if not order:
            return False

        if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order cannot be cancelled at this stage"
            )

        # Restore stock
        for item in order.items:
            variant = (
                self.db.query(ProductVariant)
                .filter(ProductVariant.id == item.product_variant_id)
                .first()
            )
            if variant:
                variant.stock_quantity += item.quantity

        # Update order status
        order.status = OrderStatus.CANCELLED
        self.db.commit()
        return True

    async def update_order_status(self, order_id: str, status: str, tracking_number: Optional[str] = None) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None

        try:
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