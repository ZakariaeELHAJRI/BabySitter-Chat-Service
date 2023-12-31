from sqlalchemy.orm import DeclarativeBase

# models
class Model(DeclarativeBase):
    pass

# import all models here

from api.models.conversation import Conversation
from api.models.message import Message