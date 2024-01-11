
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routers import message , conversation
from api.services.conversations.crud import create_conversation
from api.services.messages.crud import create_message
from api.services.webSocket.WebSocketConsumer import WebSocketConsumer, websocket_endpoint_client
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from api.database import get_db
app = FastAPI()

#uvicorn main:app --reload     


app = FastAPI()

# Configure CORS settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "zakariae"}

app.include_router(message.router, prefix="/api/chat", tags=["message"])
app.include_router(conversation.router, prefix="/api/chat", tags=["conversation"])

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    return await websocket_endpoint_client(websocket, user_id, db) 