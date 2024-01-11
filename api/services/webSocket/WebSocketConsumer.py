from typing import Dict

from sqlalchemy.orm import Session
from api.services.conversations.crud import create_conversation
from api.services.messages.crud import create_message
from fastapi import WebSocket, Depends, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
import json


class WebSocketConsumer:
    def __init__(self):
        self.connections = {}  # Dictionary to store WebSocket connections

    async def connect(self, websocket, user_id):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id):
        if user_id in self.connections:
            del self.connections[user_id]

   
    async def send_message(self, receiver_id: int,sender_id: int , invitation_data: Dict):
        receiver_id_str = str(receiver_id)  # Convert receiver_id to a string
        sender_id_str = str(sender_id)
        print("connections:", self.connections)
        if receiver_id_str in self.connections:
            print("Sending message to user", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
        
        if sender_id_str in self.connections:
            print("Sending message to user", sender_id)
            await self.connections[sender_id_str].send_json(invitation_data)
        else:
            print("User", sender_id, "is not connected")


   
    async def new_conversation(self, receiver_id: int,sender_id: int , invitation_data: Dict):
        receiver_id_str = str(receiver_id)
        sender_id_str = str(sender_id)
        if receiver_id_str in self.connections:
            print("Sending message to user with new conversation", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
        
        if sender_id_str in self.connections:
            print("Sending message to user", sender_id)
            await self.connections[sender_id_str].send_json(invitation_data)
# end class
websocket_consumer = WebSocketConsumer()

async def websocket_endpoint_client(websocket: WebSocket, user_id: int, db: Session):
        
        await websocket_consumer.connect(websocket, str(user_id))
        try:
            while True:
                ##### Receive messages from the client
                # Receive messages from the client
                #data_str = await websocket.receive_text()
                # mock data from client
                # data_str = '{"event": "message", "data": {"content": "Hello zakariae", "sender_id": 1, "receiver_id": 2, "conversation_id": 1}}'
                # mock data conversation
                ##### Receive messages from the client
                data_str = '{"event": "newConversation", "data": {"user1_id": 2, "user2_id": 3}}'
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
                    new_message_data_without_event = new_message_data.copy()
                    keys_to_exclude = ["event", "send_at", "is_read"]
                    for key in keys_to_exclude:
                        del new_message_data_without_event[key]

                    create_message(db, new_message_data_without_event)
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
                    new_conversation_data_without_event = new_conversation_data_socket.copy()
                    del new_conversation_data_without_event["event"]
                    create_conversation(db, new_conversation_data_without_event)
                    print("The conversation has been sent to the recipient")

        except WebSocketDisconnect:
            websocket_consumer.disconnect(str(user_id))
        except Exception as e:
            print(f"WebSocket Error: {str(e)}")