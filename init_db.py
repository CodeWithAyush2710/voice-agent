"""
Initialize database with sample products
"""
from db import Product, Base, Session, engine

# Create all tables
Base.metadata.create_all(engine)

# Sample hardware products
products = [
    {"code": "H001", "name": "Hammer", "rate": 250, "stock": 50},
    {"code": "C002", "name": "Cement", "rate": 400, "stock": 100},
    {"code": "N003", "name": "Nails 2 inch", "rate": 150, "stock": 200},
    {"code": "S004", "name": "Screws", "rate": 120, "stock": 500},
    {"code": "P005", "name": "Paint White", "rate": 850, "stock": 20},
    {"code": "P006", "name": "Plier", "rate": 300, "stock": 10},
    {"code": "W007", "name": "Wire bundle", "rate": 600, "stock": 5},
]

session = Session()

# Only add if not already present
for prod in products:
    existing = session.query(Product).filter_by(code=prod["code"]).first()
    if not existing:
        product = Product(
            code=prod["code"],
            name=prod["name"],
            rate=prod["rate"],
            stock=prod["stock"]
        )
        session.add(product)
        print(f"✅ Added: {prod['code']} - {prod['name']} @ {prod['rate']} (Stock: {prod['stock']})")
    else:
        # Update existing stock if necessary to make testing easier
        if existing.stock != prod["stock"]:
             existing.stock = prod["stock"]
             print(f"🔄 Updated stock for: {prod['code']} to {prod['stock']}")
        print(f"⏭️  Skipped: {prod['code']} (already exists)")

session.commit()
session.close()

print("\n📊 Database initialized successfully!")
