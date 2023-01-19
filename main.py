from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

from typing import Union
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

fake_items_db = {'items':[{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]}

@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):   
     # results = {"items": {"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        fake_items_db.update({"q": q})
    return fake_items_db
fake_items_db

@app.get("/items/{item_id}")
async def read_item(item_id: str, item: Item, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, **item.dict(), "q": q}
    return {"item_id": item_id, **item.dict()}

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax =item.price+item.tax
        item_dict.update({'price_with_tax':price_with_tax})
    return item_dict