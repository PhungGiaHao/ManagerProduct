from typing import List, Optional
from fastapi import APIRouter, File, HTTPException, Query, UploadFile , status
from app.Schema.schemas import FileUploadResponse, Product, ProductCreate, ProductInventory  # Ensure this path is correct
from database import db_dependency, get_db
from app.Model import models
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError
import magic
load_dotenv()
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
LocalStackEndPoint = os.getenv("LocalStackEndPoint")
s3_client = boto3.client(
    "s3",
    endpoint_url=LocalStackEndPoint,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

SUPPORTED_FILE_TYPES = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif',
}

router = APIRouter()

## get product with optional parameters from category , search text , pagenation , in stock level
@router.get("/", response_model=list[Product],status_code=status.HTTP_200_OK)
def read_products(db: db_dependency, 
                 category_id: int = None,
                 search: str = None, 
                 skip: int = 0, 
                 limit: int = 10, 
                 in_stock: Optional[bool] = Query(None, description="Filter products that are in stock (i.e., stock level > 0)"), ):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))
    if in_stock:
        query = query.filter(models.Product.stock_level > 0)
    result = query.offset(skip).limit(limit).all()
  
    if not result:
        raise HTTPException(status_code=404, detail="Products not found")
    return result

##Create new Product
@router.post("/", response_model=Product)
def create_product(db: db_dependency, product: ProductCreate):
    existing_product = db.query(models.Product).filter_by(name=product.name).first()
    if existing_product:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists."
        )
    category_exists = db.query(models.Category).filter_by(id=product.category_id).first()
    if not category_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )
    db_product = models.Product(name=product.name,description=product.description,price=product.price,stock_level=product.stock_level,imageurl=product.imageurl,inventory=product.inventory,category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

##Update Product
@router.put("/{product_id}", response_model=Product,status_code=status.HTTP_200_OK) 
def update_product(product_id: int, product_update: ProductCreate, db: db_dependency):
    product = db.query(models.Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    existing_product = db.query(models.Product).filter_by(name=product_update.name).first()
    if existing_product and existing_product.id != product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists."
        )
    product.name = product_update.name
    product.description = product_update.description
    product.price = product_update.price
    product.stock_level = product_update.stock_level
    product.imageurl = product_update.imageurl
    product.inventory = product_update.inventory
    product.category_id = product_update.category_id
    db.commit()
    db.refresh(product)
    return product

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Product",
    description="Delete a product by its ID. If the product does not exist, returns a 404 error."
)
def delete_product(product_id: int,  db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully."}


@router.get(
    "/inventory",
    response_model=List[ProductInventory],
    status_code=status.HTTP_200_OK,
    summary="Get Inventory Levels for All Products",
    description="Retrieve inventory levels for all products with specific fields and sorted by remaining quantity in descending order."
)
def get_all_inventory(db: db_dependency , skip: int = 0, limit: int = 10):
    # Query to get inventory levels for all products
    products = db.query(
        models.Product.id,
        models.Product.name,
        models.Product.inventory,
        models.Category.name.label('category')
        ).join(models.Category).\
            order_by(models.Product.inventory.desc()).\
            offset(skip).\
            limit(limit).\
            all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found."
        )
    
    # Select only relevant fields

    
    return products

## get inventory by id 
@router.get(
    "/inventory/{product_id}",
    response_model=ProductInventory,
    status_code=status.HTTP_200_OK,
    summary="Get Inventory Level for a Product by ID",
    description="Retrieve inventory level for a product by its ID."
)
def get_inventory_by_id(product_id: int, db: db_dependency):
    product = db.query(
        models.Product.id,
        models.Product.name,
        models.Product.inventory,
        models.Category.name.label('category')
    ).join(models.Category).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    return product


## upload file to s3 bucket localstack ,support file type image upload
@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a File to S3 Bucket",
    description="Upload a file to the S3 bucket using the LocalStack endpoint,support image upload only"
)
async def upload_file(file: UploadFile = File(...)):

    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")
    content = await file.read()
    file_size = len(content)
    if not (0 < file_size <= 1 * 1024 * 1024):
        raise HTTPException(status_code=400, detail="File size must be between 0 and 1 MB")

    # Check file type
 
    file_type = magic.from_buffer(buffer=content, mime=True)
    print(f"File type: {file_type}")

    # Validate that the file is an image
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Only image files are supported")



    file.file.seek(0) 
    file_name = f"{file.filename}"
    
    try:
        # Upload file to S3
        s3_client.upload_fileobj(file.file, S3_BUCKET, file_name)
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")

    # Generate a presigned URL for accessing the file
    file_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET, 'Key': file_name},
        ExpiresIn=3600  # URL expiration time in seconds
    )

    return FileUploadResponse(file_url=file_url)
   
## upload file update product imageurl with id 
@router.put(
    "/{product_id}/upload",
    status_code=status.HTTP_200_OK,
    summary="Upload a File to S3 Bucket and Update Product Image URL",
    description="Upload a file to the S3 bucket using the LocalStack endpoint and update the product image URL."
)
async def upload_file_and_update_product_image(db: db_dependency,product_id: int, file: UploadFile = File(...)):
    result = await upload_file(file)
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    product.imageurl = result.file_url
    db.commit()
    db.refresh(product)
    return product
    

    
def search_inventory():
    ##search product investory < 100
    db = next(get_db())
    products = db.query(models.Product).filter(models.Product.inventory < 50 ).all()
    return products


