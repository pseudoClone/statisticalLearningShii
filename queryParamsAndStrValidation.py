from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(q:Annotated[str | None, Query(max_length=24, 
                                       min_length=2, title="ShitParameter",
                                       alias='shit-param')] = None):
    results = {"items":[{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Now we gonna enforace rules to q if it is included
