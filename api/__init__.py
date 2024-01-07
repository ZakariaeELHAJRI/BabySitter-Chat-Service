from typing import Union

from fastapi import FastAPI
from api.routers import message , conversation

app = FastAPI()

#uvicorn main:app --reload     

@app.get("/")
def read_root():
    return {"Hello": "World zakariae"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(message.router, prefix="/api/chat", tags=["message"])
app.include_router(conversation.router, prefix="/api/chat", tags=["conversation"])