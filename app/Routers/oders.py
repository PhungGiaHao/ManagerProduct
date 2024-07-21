from decimal import Decimal
from fastapi import APIRouter, File, HTTPException, Query, UploadFile , status
from app.Schema.schemas import FileUploadResponse, OrderCreate, OrderResponse, Product, ProductCreate, ProductInventory  # Ensure this path is correct
from app.utils.shippingcost import calculate_shipping_cost
from database import db_dependency, get_db
from app.Model import models

router = APIRouter()    

##


##Create new Order
@router.post("/createOrder", response_model=OrderResponse)
def create_order(db: db_dependency, order: OrderCreate):
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if product.inventory < order.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock"
        )
    product.inventory -= order.quantity
    shipping_cost = calculate_shipping_cost()
    total_cost =(product.price * order.quantity) + Decimal(shipping_cost)
    db_order = models.Order(product_id = order.product_id, quantity = order.quantity, total_cost = total_cost, shipping_cost = shipping_cost, weight = order.weight)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order