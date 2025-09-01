from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_ID}")
async def read_items(item_ID:int):
    return {"item_id": item_ID}
