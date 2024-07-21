import logging
import time
from typing import Annotated
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from requests import Session
from app.Model import models
from app.utils.dynamodb import create_table, log_api_call
from app.utils.s3_sqs import send_message_low_stock
from database import engine, get_db
from app.Routers import auth, category, product,oders
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.security import HTTPBearer
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)
@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info('App started')
    create_table()
    scheduler = BackgroundScheduler()
    scheduler.add_job(id='Scheduled Task', func=send_message_low_stock, trigger='interval', seconds=1000)
    scheduler.start()
    yield 
    logger.info('App stopped')
    # scheduler.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def track_api_calls(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    call_id = str(uuid4())
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
    
    # Log the API call to DynamoDB
    log_api_call(call_id, timestamp, request.method, request.url.path, response.status_code, process_time)
    logger.info(f'API call {response.status_code} logged in {process_time:.4f} seconds')
    return response

models.Base.metadata.create_all(bind=engine)
get_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(category.router, prefix="/categories", tags=["categories"],dependencies=[Depends(reusable_oauth2)])
app.include_router(product.router, prefix="/products", tags=["products"])
app.include_router(oders.router, prefix="/orders", tags=["orders"])   
@app.get('/')
def root():
    return {"message": "Hello World"}
