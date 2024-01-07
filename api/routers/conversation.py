from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.conversation import Conversation
from api.database import get_db
from api.services.conversations.crud import  create_conversation, get_conversation, update_conversation, delete_conversation ,get_conversations,get_conversations_by_user


router = APIRouter()

@router.post("/conversation")
def create_new_conversation( conversation_data: dict, db: Session = Depends(get_db)):
    return create_conversation(db,conversation_data)

@router.get("/conversation/{conversation_id}")
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = get_conversation(db=db, conversation_id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.put("/conversation/{conversation_id}")
def update_conversation(conversation_id: int, conversation_data: dict, db: Session = Depends(get_db)):
    db_conversation = update_conversation(db=db, conversation_id=conversation_id, conversation_data=conversation_data)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.delete("/conversation/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conversation = delete_conversation(db=db, conversation_id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

@router.get("/conversations")
def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = get_conversations(db=db, skip=skip, limit=limit)
    return conversations

@router.get("/conversations/user/{user_id}")
def read_conversations_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = get_conversations_by_user(db=db, user_id=user_id, skip=skip, limit=limit)
    return conversations

