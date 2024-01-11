from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.message import Message
from api.database import get_db
from api.services.messages.crud import  create_message, get_message, update_message, delete_message ,get_messages,get_messages_by_conversation,get_messages_by_user,get_unread_messages_by_user,get_unread_messages_by_conversation


router = APIRouter()

@router.post("/message")
def create_new_message( message_data: dict, db: Session = Depends(get_db)):
    return create_message(db,message_data)

@router.get("/message/{message_id}")
def read_message(message_id: int, db: Session = Depends(get_db)):
    db_message = get_message(db,message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.put("/message/{message_id}")
def update_message(message_id: int, message_data: dict, db: Session = Depends(get_db)):
    db_message = update_message(db,message_id,message_data)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.delete("/message/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = delete_message(db,message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@router.get("/messages")
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_messages(db,skip,limit)
    return messages

@router.get("/messages/conversation/{conversation_id}")
def read_messages_by_conversation(conversation_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_messages_by_conversation(db,conversation_id,skip,limit)
    return messages

@router.get("/messages/user/{user_id}")
def read_messages_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_messages_by_user(db,user_id,skip,limit)
    return messages

@router.get("/messages/unread/user/{user_id}")
def read_unread_messages_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_unread_messages_by_user(db,user_id,skip,limit)
    return messages

@router.get("/messages/unread/conversation/{conversation_id}")
def read_unread_messages_by_conversation(conversation_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = get_unread_messages_by_conversation(db,conversation_id,skip,limit)
    return messages