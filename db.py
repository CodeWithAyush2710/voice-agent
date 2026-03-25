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

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    product_code = Column(String)
    quantity = Column(Integer)
    rate = Column(Float)
    amount = Column(Float)

Base.metadata.create_all(engine)

def get_rate(product_code):
    session = Session()
    product = session.query(Product).filter_by(code=product_code).first()
    return product.rate if product else None

def save_order(product_code, quantity, rate, amount):
    session = Session()
    order = Order(
        product_code=product_code,
        quantity=quantity,
        rate=rate,
        amount=amount
    )
    session.add(order)
    session.commit()