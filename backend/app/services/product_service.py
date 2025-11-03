from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from fastapi import HTTPException, status
from typing import List, Optional
from decimal import Decimal
from app.models.product import Product, ProductVariant
from app.schemas import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 20,
        sport: Optional[str] = None,
        team: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: Optional[str] = "created_at"
    ) -> List[Product]:
        query = self.db.query(Product).filter(Product.is_active == True)

        # Apply filters
        if sport:
            query = query.filter(Product.sport.ilike(f"%{sport}%"))
        if team:
            query = query.filter(Product.team.ilike(f"%{team}%"))
        if min_price is not None:
            query = query.filter(Product.base_price >= Decimal(min_price))
        if max_price is not None:
            query = query.filter(Product.base_price <= Decimal(max_price))

        # Apply sorting
        if sort_by == "price_asc":
            query = query.order_by(asc(Product.base_price))
        elif sort_by == "price_desc":
            query = query.order_by(desc(Product.base_price))
        elif sort_by == "newest":
            query = query.order_by(desc(Product.created_at))
        elif sort_by == "rating":
            query = query.order_by(desc(Product.average_rating))
        else:
            query = query.order_by(desc(Product.created_at))

        return query.offset(skip).limit(limit).all()

    async def get_featured_products(self, limit: int = 8) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.is_active == True)
            .order_by(desc(Product.average_rating))
            .limit(limit)
            .all()
        )

    async def get_new_arrivals(self, limit: int = 8) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.is_active == True)
            .order_by(desc(Product.created_at))
            .limit(limit)
            .all()
        )

    async def search_products(self, query: str, limit: int = 20) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(
                and_(
                    Product.is_active == True,
                    or_(
                        Product.name.ilike(f"%{query}%"),
                        Product.team.ilike(f"%{query}%"),
                        Product.player.ilike(f"%{query}%"),
                        Product.sport.ilike(f"%{query}%"),
                        Product.brand.ilike(f"%{query}%")
                    )
                )
            )
            .order_by(desc(Product.average_rating))
            .limit(limit)
            .all()
        )

    async def get_product_by_slug(self, slug: str) -> Optional[Product]:
        return (
            self.db.query(Product)
            .filter(and_(Product.slug == slug, Product.is_active == True))
            .first()
        )

    async def create_product(self, product_data: ProductCreate) -> Product:
        # Check if slug already exists
        existing_product = self.db.query(Product).filter(Product.slug == product_data.slug).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this slug already exists"
            )

        # Create product
        db_product = Product(
            name=product_data.name,
            slug=product_data.slug,
            description=product_data.description,
            team=product_data.team,
            player=product_data.player,
            sport=product_data.sport,
            brand=product_data.brand,
            base_price=product_data.base_price,
            sale_price=product_data.sale_price,
            material=product_data.material,
            care_instructions=product_data.care_instructions,
        )

        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)

        # Create variants
        for variant_data in product_data.variants:
            db_variant = ProductVariant(
                product_id=db_product.id,
                size=variant_data.size,
                color=variant_data.color,
                sku=variant_data.sku,
                stock_quantity=variant_data.stock_quantity,
                price=variant_data.price,
                image_urls=variant_data.image_urls,
            )
            self.db.add(db_variant)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[Product]:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        # Update fields
        for field, value in product_data.dict(exclude_unset=True).items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    async def delete_product(self, product_id: str) -> bool:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False

        # Soft delete
        product.is_active = False
        self.db.commit()
        return True

    async def get_categories(self) -> List[str]:
        from sqlalchemy import func
        result = (
            self.db.query(Product.sport)
            .filter(Product.is_active == True)
            .distinct()
            .all()
        )
        return [row[0] for row in result]

    async def get_teams(self, sport: Optional[str] = None) -> List[str]:
        from sqlalchemy import func
        query = self.db.query(Product.team).filter(Product.is_active == True)
        if sport:
            query = query.filter(Product.sport == sport)

        result = query.distinct().all()
        return [row[0] for row in result]