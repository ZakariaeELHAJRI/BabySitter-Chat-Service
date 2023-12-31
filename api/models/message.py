from api.models import Model
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime, func , Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

class Message(Model):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)
    receiver_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    send_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    # Add a foreign key reference to the Conversation model
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey('conversation.id'), nullable=False)

    # Relationship to link this Message model to the conversation
    conversation = relationship("Conversation", back_populates="messages")

    def __init__(self, content: str, sender_id: int, receiver_id: int, conversation_id: int):
        self.content = content
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.conversation_id = conversation_id

    def __str__(self):
        return f"Message from User {self.sender_id} to User {self.receiver_id}"