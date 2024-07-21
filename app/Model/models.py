from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(DECIMAL(10, 2), index=True)
    stock_level = Column(Integer, index=True)
    imageurl = Column(String, index=True)  
    inventory = Column(Integer, index=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="products")

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    weight = Column(Float, index=True, default=0.0)
    shipping_cost = Column(DECIMAL(10, 2), default=0.0)
    total_cost = Column(DECIMAL(10, 2), default=0.0)
    product = relationship("Product")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
