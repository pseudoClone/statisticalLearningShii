from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{items_id}")
async def shitItems(items_id: int, q:str | None = None):
    if q:
        return {"item_id":items_id, "q": q}
    return {"item_id":items_id}
