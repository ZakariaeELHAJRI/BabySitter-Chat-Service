from sqlalchemy.orm import Session

from api.models.message import Message


def create_message(db: Session,message_data : dict):
    db_message = Message(**message_data)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def update_message(db: Session, message_id: int, message_data: dict):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        return None
    for key, value in message_data.items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        return None
    db.delete(db_message)
    db.commit()
    return db_message

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).offset(skip).limit(limit).all()

def get_messages_by_conversation(db: Session, conversation_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.conversation_id == conversation_id).offset(skip).limit(limit).all()

def get_messages_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.sender_id == user_id).offset(skip).limit(limit).all()

def get_unread_messages_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.sender_id == user_id).filter(Message.is_read == False).offset(skip).limit(limit).all()

def get_unread_messages_by_conversation(db: Session, conversation_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.conversation_id == conversation_id).filter(Message.is_read == False).offset(skip).limit(limit).all()
