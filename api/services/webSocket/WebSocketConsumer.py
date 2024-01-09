from typing import Dict

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
            print("Sending message to user", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
        
        if sender_id_str in self.connections:
            print("Sending message to user", sender_id)
            await self.connections[sender_id_str].send_json(invitation_data)
