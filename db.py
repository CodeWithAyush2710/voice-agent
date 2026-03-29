from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    rate = Column(Float)
    stock = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    quantity = Column(Integer)
    rate = Column(Float)
    amount = Column(Float)
    phone = Column(String)

class Backorder(Base):
    __tablename__ = "backorders"
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    quantity = Column(Integer)
    phone = Column(String)
    status = Column(String, default="Pending")

Base.metadata.create_all(engine)

def get_product_by_name(item_name):
    session = Session()
    # Simple case-insensitive exact/partial match
    product = session.query(Product).filter(Product.name.ilike(f"%{item_name}%")).first()
    return product

def deduct_stock(product_id, quantity):
    session = Session()
    product = session.query(Product).filter_by(id=product_id).first()
    if product and product.stock >= quantity:
        product.stock -= quantity
        session.commit()
        return True
    return False

def save_order(item_name, quantity, rate, amount, phone):
    session = Session()
    order = Order(
        item_name=item_name,
        quantity=quantity,
        rate=rate,
        amount=amount,
        phone=phone
    )
    session.add(order)
    session.commit()

def save_backorder(item_name, quantity, phone):
    session = Session()
    backorder = Backorder(
        item_name=item_name,
        quantity=quantity,
        phone=phone
    )
    session.add(backorder)
    session.commit()