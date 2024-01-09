import json
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.routers import message , conversation
from api.services.messages.crud import create_message
from api.services.webSocket.WebSocketConsumer import WebSocketConsumer
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from api.database import get_db
app = FastAPI()

#uvicorn main:app --reload     
websocket_consumer = WebSocketConsumer()

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
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):

    await websocket_consumer.connect(websocket, str(user_id))
    try:
        while True:
            # Receive messages from the client
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            event_name = data.get("event")

            if event_name == "message":
                print("data from client:", data)
                content = data['data'].get("content")
                sender_id = data['data'].get("sender_id")
                receiver_id = data['data'].get("receiver_id")
                time = data['data'].get("time")
                conversation_id = data['data'].get("conversation_id")
                is_read = data['data'].get("is_read")

                new_message_data = {
                    "content": content,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "send_at": time,#  just to use them when the user recieve the socket in his frontend 
                    "conversation_id": conversation_id,
                    "is_read": is_read,#  just to use them when the user recieve the socket in his frontend 
                    "event": "message"
                }
                print("New message:", new_message_data)
                await websocket_consumer.send_message(int(receiver_id),int(sender_id), new_message_data)
                create_message(db, new_message_data)
                print("The message has been sent to the recipient")

            elif event_name == "newConversation":
                user1_id = data['data'].get("user1_id")
                user2_id = data['data'].get("user2_id")
                print('data new conversation:', data)

                new_conversation_data_socket = {
                    "user1_id": user1_id,
                    "user2_id": user2_id,
                    "event": "newConversation"
                }
                print("New conversation:", new_conversation_data_socket)
                await websocket_consumer.new_conversation(int(user1_id),int(user2_id), new_conversation_data_socket)
                print("The conversation has been sent to the recipient")

    except WebSocketDisconnect:
        websocket_consumer.disconnect(str(user_id))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")


@app.get("/")
def read_root():
    return {"Hello": "World zakariae"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(message.router, prefix="/api/chat", tags=["message"])
app.include_router(conversation.router, prefix="/api/chat", tags=["conversation"])