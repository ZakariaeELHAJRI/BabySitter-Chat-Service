from sqlalchemy.orm import Session

from api.models.conversation import  Conversation


def create_conversation(db: Session, conversation_data: dict):
    db_conversation = Conversation(**conversation_data)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def update_conversation(db: Session, conversation_id: int, conversation_data: dict):
    db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if db_conversation is None:
        return None
    for key, value in conversation_data.items():
        setattr(db_conversation, key, value)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def delete_conversation(db: Session, conversation_id: int):
    db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if db_conversation is None:
        return None
    db.delete(db_conversation)
    db.commit()
    return db_conversation

def get_conversations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Conversation).offset(skip).limit(limit).all()

def get_conversations_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Conversation).filter(Conversation.user1_id == user_id).offset(skip).limit(limit).all()

