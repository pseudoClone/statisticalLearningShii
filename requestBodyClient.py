from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name : str
    description: str | None = None
    price : float
    tax : float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump() # model_dump instead of dict
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"Price_With_Tax": price_with_tax})
    return item_dict
