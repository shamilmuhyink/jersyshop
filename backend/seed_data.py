import asyncio
import sys
import os
from sqlalchemy.orm import Session
from decimal import Decimal
from uuid import uuid4

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.database import SessionLocal, engine
from app.models import Base, Product, ProductVariant, User
from app.services.auth_service import AuthService

# Sample jersey data
SAMPLE_JERSEYS = [
    {
        "name": "Tom Brady Buccaneers Jersey",
        "slug": "tom-brady-buccaneers-jersey",
        "description": "Official Tom Brady Tampa Bay Buccaneers home jersey. Features authentic team colors and numbering.",
        "team": "Tampa Bay Buccaneers",
        "player": "Tom Brady",
        "sport": "Football",
        "brand": "Nike",
        "base_price": Decimal("199.99"),
        "material": "100% Polyester Mesh",
        "care_instructions": "Machine wash cold, tumble dry low",
        "variants": [
            {"size": "S", "sku": "TB-BUC-S-BLUE", "stock_quantity": 50, "price": Decimal("199.99")},
            {"size": "M", "sku": "TB-BUC-M-BLUE", "stock_quantity": 75, "price": Decimal("199.99")},
            {"size": "L", "sku": "TB-BUC-L-BLUE", "stock_quantity": 100, "price": Decimal("199.99")},
            {"size": "XL", "sku": "TB-BUC-XL-BLUE", "stock_quantity": 75, "price": Decimal("199.99")},
            {"size": "XXL", "sku": "TB-BUC-XXL-BLUE", "stock_quantity": 50, "price": Decimal("199.99")},
        ]
    },
    {
        "name": "Patrick Mahomes Chiefs Jersey",
        "slug": "patrick-mahomes-chiefs-jersey",
        "description": "Patrick Mahomes Kansas City Chiefs red jersey. Official NFL gear with quality construction.",
        "team": "Kansas City Chiefs",
        "player": "Patrick Mahomes",
        "sport": "Football",
        "brand": "Nike",
        "base_price": Decimal("189.99"),
        "sale_price": Decimal("169.99"),
        "material": "Performance Mesh",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "PM-CHIEFS-S-RED", "stock_quantity": 40, "price": Decimal("189.99")},
            {"size": "M", "sku": "PM-CHIEFS-M-RED", "stock_quantity": 60, "price": Decimal("189.99")},
            {"size": "L", "sku": "PM-CHIEFS-L-RED", "stock_quantity": 80, "price": Decimal("189.99")},
            {"size": "XL", "sku": "PM-CHIEFS-XL-RED", "stock_quantity": 70, "price": Decimal("189.99")},
            {"size": "XXL", "sku": "PM-CHIEFS-XXL-RED", "stock_quantity": 45, "price": Decimal("189.99")},
            {"size": "XXXL", "sku": "PM-CHIEFS-XXXL-RED", "stock_quantity": 25, "price": Decimal("189.99")},
        ]
    },
    {
        "name": "LeBron James Lakers Jersey",
        "slug": "lebron-james-lakers-jersey",
        "description": "LeBron James Los Angeles Lakers gold and purple jersey. Authentic NBA apparel.",
        "team": "Los Angeles Lakers",
        "player": "LeBron James",
        "sport": "Basketball",
        "brand": "Nike",
        "base_price": Decimal("179.99"),
        "material": "Dri-FIT Technology",
        "care_instructions": "Machine wash cold, tumble dry low",
        "variants": [
            {"size": "S", "sku": "LJ-LAKERS-S-GOLD", "stock_quantity": 35, "price": Decimal("179.99")},
            {"size": "M", "sku": "LJ-LAKERS-M-GOLD", "stock_quantity": 55, "price": Decimal("179.99")},
            {"size": "L", "sku": "LJ-LAKERS-L-GOLD", "stock_quantity": 75, "price": Decimal("179.99")},
            {"size": "XL", "sku": "LJ-LAKERS-XL-GOLD", "stock_quantity": 65, "price": Decimal("179.99")},
            {"size": "XXL", "sku": "LJ-LAKERS-XXL-GOLD", "stock_quantity": 40, "price": Decimal("179.99")},
        ]
    },
    {
        "name": "Kevin Durant Nets Jersey",
        "slug": "kevin-durant-nets-jersey",
        "description": "Kevin Durant Brooklyn Nets black and white jersey. Official NBA merchandise.",
        "team": "Brooklyn Nets",
        "player": "Kevin Durant",
        "sport": "Basketball",
        "brand": "Nike",
        "base_price": Decimal("169.99"),
        "material": "Climalite Fabric",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "KD-NETS-S-BLK", "stock_quantity": 30, "price": Decimal("169.99")},
            {"size": "M", "sku": "KD-NETS-M-BLK", "stock_quantity": 45, "price": Decimal("169.99")},
            {"size": "L", "sku": "KD-NETS-L-BLK", "stock_quantity": 60, "price": Decimal("169.99")},
            {"size": "XL", "sku": "KD-NETS-XL-BLK", "stock_quantity": 50, "price": Decimal("169.99")},
        ]
    },
    {
        "name": "Aaron Judge Yankees Jersey",
        "slug": "aaron-judge-yankees-jersey",
        "description": "Aaron Judge New York Yankees pinstripe jersey. Classic MLB baseball uniform.",
        "team": "New York Yankees",
        "player": "Aaron Judge",
        "sport": "Baseball",
        "brand": "Majestic",
        "base_price": Decimal("159.99"),
        "material": "Authentic Jersey Material",
        "care_instructions": "Dry clean only",
        "variants": [
            {"size": "S", "sku": "AJ-YAN-S-NVY", "stock_quantity": 25, "price": Decimal("159.99")},
            {"size": "M", "sku": "AJ-YAN-M-NVY", "stock_quantity": 40, "price": Decimal("159.99")},
            {"size": "L", "sku": "AJ-YAN-L-NVY", "stock_quantity": 55, "price": Decimal("159.99")},
            {"size": "XL", "sku": "AJ-YAN-XL-NVY", "stock_quantity": 45, "price": Decimal("159.99")},
            {"size": "XXL", "sku": "AJ-YAN-XXL-NVY", "stock_quantity": 30, "price": Decimal("159.99")},
        ]
    },
    {
        "name": "Mike Trout Angels Jersey",
        "slug": "mike-trout-angels-jersey",
        "description": "Mike Trout Los Angeles Angels red jersey. Official MLB apparel with quality stitching.",
        "team": "Los Angeles Angels",
        "player": "Mike Trout",
        "sport": "Baseball",
        "brand": "Majestic",
        "base_price": Decimal("149.99"),
        "material": "Cool Base Technology",
        "care_instructions": "Machine wash cold, tumble dry low",
        "variants": [
            {"size": "S", "sku": "MT-ANG-S-RED", "stock_quantity": 20, "price": Decimal("149.99")},
            {"size": "M", "sku": "MT-ANG-M-RED", "stock_quantity": 35, "price": Decimal("149.99")},
            {"size": "L", "sku": "MT-ANG-L-RED", "stock_quantity": 50, "price": Decimal("149.99")},
            {"size": "XL", "sku": "MT-ANG-XL-RED", "stock_quantity": 40, "price": Decimal("149.99")},
        ]
    },
    {
        "name": "Lionel Messi PSG Jersey",
        "slug": "lionel-messi-psg-jersey",
        "description": "Lionel Messi Paris Saint-Germain home jersey. Premium soccer apparel.",
        "team": "Paris Saint-Germain",
        "player": "Lionel Messi",
        "sport": "Soccer",
        "brand": "Nike",
        "base_price": Decimal("179.99"),
        "material": "Official Match Quality",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "LM-PSG-S-BLU", "stock_quantity": 45, "price": Decimal("179.99")},
            {"size": "M", "sku": "LM-PSG-M-BLU", "stock_quantity": 70, "price": Decimal("179.99")},
            {"size": "L", "sku": "LM-PSG-L-BLU", "stock_quantity": 85, "price": Decimal("179.99")},
            {"size": "XL", "sku": "LM-PSG-XL-BLU", "stock_quantity": 65, "price": Decimal("179.99")},
        ]
    },
    {
        "name": "Cristiano Ronaldo Manchester United Jersey",
        "slug": "cristiano-ronaldo-manchester-united-jersey",
        "description": "Cristiano Ronaldo Manchester United red jersey. Iconic soccer apparel.",
        "team": "Manchester United",
        "player": "Cristiano Ronaldo",
        "sport": "Soccer",
        "brand": "Adidas",
        "base_price": Decimal("189.99"),
        "material": "Stadium Replica",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "CR-MU-S-RED", "stock_quantity": 40, "price": Decimal("189.99")},
            {"size": "M", "sku": "CR-MU-M-RED", "stock_quantity": 60, "price": Decimal("189.99")},
            {"size": "L", "sku": "CR-MU-L-RED", "stock_quantity": 80, "price": Decimal("189.99")},
            {"size": "XL", "sku": "CR-MU-XL-RED", "stock_quantity": 70, "price": Decimal("189.99")},
            {"size": "XXL", "sku": "CR-MU-XXL-RED", "stock_quantity": 45, "price": Decimal("189.99")},
        ]
    },
    {
        "name": "Connor McDavid Oilers Jersey",
        "slug": "connor-mcdavid-oilers-jersey",
        "description": "Connor McDavid Edmonton Oilers blue and orange jersey. Official NHL gear.",
        "team": "Edmonton Oilers",
        "player": "Connor McDavid",
        "sport": "Hockey",
        "brand": "Adidas",
        "base_price": Decimal("169.99"),
        "material": "Premier Jersey Fabric",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "CM-OIL-S-BLU", "stock_quantity": 30, "price": Decimal("169.99")},
            {"size": "M", "sku": "CM-OIL-M-BLU", "stock_quantity": 45, "price": Decimal("169.99")},
            {"size": "L", "sku": "CM-OIL-L-BLU", "stock_quantity": 65, "price": Decimal("169.99")},
            {"size": "XL", "sku": "CM-OIL-XL-BLU", "stock_quantity": 55, "price": Decimal("169.99")},
            {"size": "XXL", "sku": "CM-OIL-XXL-BLU", "stock_quantity": 35, "price": Decimal("169.99")},
        ]
    },
    {
        "name": "Sidney Crosby Penguins Jersey",
        "slug": "sidney-crosby-penguins-jersey",
        "description": "Sidney Crosby Pittsburgh Penguins black and gold jersey. Authentic NHL merchandise.",
        "team": "Pittsburgh Penguins",
        "player": "Sidney Crosby",
        "sport": "Hockey",
        "brand": "Adidas",
        "base_price": Decimal("159.99"),
        "material": "Authentic Hockey Jersey",
        "care_instructions": "Dry clean recommended",
        "variants": [
            {"size": "S", "sku": "SC-PENS-S-BLK", "stock_quantity": 25, "price": Decimal("159.99")},
            {"size": "M", "sku": "SC-PENS-M-BLK", "stock_quantity": 40, "price": Decimal("159.99")},
            {"size": "L", "sku": "SC-PENS-L-BLK", "stock_quantity": 55, "price": Decimal("159.99")},
            {"size": "XL", "sku": "SC-PENS-XL-BLK", "stock_quantity": 45, "price": Decimal("159.99")},
        ]
    },
    {
        "name": "Michael Jordan Bulls Jersey (Classic)",
        "slug": "michael-jordan-bulls-jersey-classic",
        "description": "Michael Jordan Chicago Bulls red and black jersey. Classic basketball legend.",
        "team": "Chicago Bulls",
        "player": "Michael Jordan",
        "sport": "Basketball",
        "brand": "Nike",
        "base_price": Decimal("199.99"),
        "sale_price": Decimal("179.99"),
        "material": "Authentic Throwback Material",
        "care_instructions": "Dry clean only",
        "variants": [
            {"size": "S", "sku": "MJ-BULLS-S-RED", "stock_quantity": 50, "price": Decimal("199.99")},
            {"size": "M", "sku": "MJ-BULLS-M-RED", "stock_quantity": 75, "price": Decimal("199.99")},
            {"size": "L", "sku": "MJ-BULLS-L-RED", "stock_quantity": 100, "price": Decimal("199.99")},
            {"size": "XL", "sku": "MJ-BULLS-XL-RED", "stock_quantity": 85, "price": Decimal("199.99")},
            {"size": "XXL", "sku": "MJ-BULLS-XXL-RED", "stock_quantity": 60, "price": Decimal("199.99")},
        ]
    },
    {
        "name": "Kobe Bryant Lakers Jersey (Classic)",
        "slug": "kobe-bryant-lakers-jersey-classic",
        "description": "Kobe Bryant Los Angeles Lakers purple and gold jersey. Tribute to a basketball legend.",
        "team": "Los Angeles Lakers",
        "player": "Kobe Bryant",
        "sport": "Basketball",
        "brand": "Nike",
        "base_price": Decimal("189.99"),
        "material": "Legacy Jersey Material",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "KB-LAKERS-S-PUR", "stock_quantity": 45, "price": Decimal("189.99")},
            {"size": "M", "sku": "KB-LAKERS-M-PUR", "stock_quantity": 70, "price": Decimal("189.99")},
            {"size": "L", "sku": "KB-LAKERS-L-PUR", "stock_quantity": 90, "price": Decimal("189.99")},
            {"size": "XL", "sku": "KB-LAKERS-XL-PUR", "stock_quantity": 75, "price": Decimal("189.99")},
            {"size": "XXL", "sku": "KB-LAKERS-XXL-PUR", "stock_quantity": 55, "price": Decimal("189.99")},
        ]
    },
    {
        "name": "Dak Prescott Cowboys Jersey",
        "slug": "dak-prescott-cowboys-jersey",
        "description": "Dak Prescott Dallas Cowboys blue and white jersey. America's team official gear.",
        "team": "Dallas Cowboys",
        "player": "Dak Prescott",
        "sport": "Football",
        "brand": "Nike",
        "base_price": Decimal("179.99"),
        "material": "Game Day Jersey",
        "care_instructions": "Machine wash cold, tumble dry low",
        "variants": [
            {"size": "S", "sku": "DP-COW-S-BLU", "stock_quantity": 35, "price": Decimal("179.99")},
            {"size": "M", "sku": "DP-COW-M-BLU", "stock_quantity": 55, "price": Decimal("179.99")},
            {"size": "L", "sku": "DP-COW-L-BLU", "stock_quantity": 75, "price": Decimal("179.99")},
            {"size": "XL", "sku": "DP-COW-XL-BLU", "stock_quantity": 65, "price": Decimal("179.99")},
            {"size": "XXL", "sku": "DP-COW-XXL-BLU", "stock_quantity": 40, "price": Decimal("179.99")},
        ]
    },
    {
        "name": "Stephen Curry Warriors Jersey",
        "slug": "stephen-curry-warriors-jersey",
        "description": "Stephen Curry Golden State Warriors blue and gold jersey. Championship caliber gear.",
        "team": "Golden State Warriors",
        "player": "Stephen Curry",
        "sport": "Basketball",
        "brand": "Nike",
        "base_price": Decimal("169.99"),
        "material": "Championship Edition Fabric",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "SC-WAR-S-BLU", "stock_quantity": 30, "price": Decimal("169.99")},
            {"size": "M", "sku": "SC-WAR-M-BLU", "stock_quantity": 50, "price": Decimal("169.99")},
            {"size": "L", "sku": "SC-WAR-L-BLU", "stock_quantity": 70, "price": Decimal("169.99")},
            {"size": "XL", "sku": "SC-WAR-XL-BLU", "stock_quantity": 60, "price": Decimal("169.99")},
            {"size": "XXL", "sku": "SC-WAR-XXL-BLU", "stock_quantity": 35, "price": Decimal("169.99")},
        ]
    },
    {
        "name": "Neymar Jr. Brazil National Jersey",
        "slug": "neymar-brazil-national-jersey",
        "description": "Neymar Jr. Brazil national team yellow jersey. World Cup quality soccer apparel.",
        "team": "Brazil National Team",
        "player": "Neymar Jr.",
        "sport": "Soccer",
        "brand": "Nike",
        "base_price": Decimal("159.99"),
        "material": "National Team Fabric",
        "care_instructions": "Machine wash cold, hang dry",
        "variants": [
            {"size": "S", "sku": "NJ-BRZ-S-YEL", "stock_quantity": 40, "price": Decimal("159.99")},
            {"size": "M", "sku": "NJ-BRZ-M-YEL", "stock_quantity": 60, "price": Decimal("159.99")},
            {"size": "L", "sku": "NJ-BRZ-L-YEL", "stock_quantity": 80, "price": Decimal("159.99")},
            {"size": "XL", "sku": "NJ-BRZ-XL-YEL", "stock_quantity": 70, "price": Decimal("159.99")},
        ]
    }
]

def create_sample_data():
    """Create sample products and admin user"""
    db = SessionLocal()

    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Check if data already exists
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"Database already has {existing_products} products. Skipping seed.")
            return

        print("Creating sample jersey data...")

        # Create products
        for jersey_data in SAMPLE_JERSEYS:
            # Create product
            product = Product(
                name=jersey_data["name"],
                slug=jersey_data["slug"],
                description=jersey_data["description"],
                team=jersey_data["team"],
                player=jersey_data["player"],
                sport=jersey_data["sport"],
                brand=jersey_data["brand"],
                base_price=jersey_data["base_price"],
                sale_price=jersey_data.get("sale_price"),
                material=jersey_data["material"],
                care_instructions=jersey_data["care_instructions"],
                average_rating=4.5,  # Sample rating
                review_count=25,     # Sample review count
                is_active=True
            )

            db.add(product)
            db.flush()  # Get the product ID

            # Create variants
            for variant_data in jersey_data["variants"]:
                variant = ProductVariant(
                    product_id=product.id,
                    size=variant_data["size"],
                    sku=variant_data["sku"],
                    stock_quantity=variant_data["stock_quantity"],
                    price=variant_data["price"],
                    image_urls=[
                        f"https://example.com/images/{jersey_data['slug']}-{variant_data['size'].lower()}-front.jpg",
                        f"https://example.com/images/{jersey_data['slug']}-{variant_data['size'].lower()}-back.jpg"
                    ]
                )
                db.add(variant)

            print(f"Created product: {jersey_data['name']}")

        # Create admin user
        auth_service = AuthService(db)
        admin_data = {
            "email": "admin@example.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User"
        }

        try:
            admin_user = await auth_service.register(admin_data)
            admin_user.is_admin = True
            db.commit()
            print(f"Created admin user: {admin_user.email}")
        except Exception as e:
            print(f"Admin user might already exist: {e}")

        # Create regular user
        user_data = {
            "email": "user@example.com",
            "password": "user123",
            "first_name": "Test",
            "last_name": "User"
        }

        try:
            test_user = await auth_service.register(user_data)
            db.commit()
            print(f"Created test user: {test_user.email}")
        except Exception as e:
            print(f"Test user might already exist: {e}")

        db.commit()
        print(f"Successfully created {len(SAMPLE_JERSEYS)} sample products!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()