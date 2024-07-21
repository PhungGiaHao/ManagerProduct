

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.s3_sqs import delete_message_from_sqs, read_messages_from_sqs, send_message_low_stock
router = APIRouter()
class Message(BaseModel):
    content: str
@router.post("/send_message")
async def send_message(message: Message):
    try:
        send_message_low_stock()
        return {"message": "Message sent to SQS successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/receive_messages")
async def receive_messages():
    try:
        messages = read_messages_from_sqs()
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_message/{receipt_handle}")
async def delete_message(receipt_handle: str):
    try:
        delete_message_from_sqs(receipt_handle)
        return {"message": "Message deleted from SQS successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))