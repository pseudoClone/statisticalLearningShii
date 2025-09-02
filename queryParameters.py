# Using parameters in functions that are not path parameters make query parameters
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items")
async def get_items(skip:int= 0, limit:int=10):
    return fake_items_db[skip:skip+limit]
