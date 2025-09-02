import random
from typing import Annotated
from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_validation(id: str):
    if not id.startswith(("imdb-", "isbn-")):
        raise ValueError("Invalid ID format, must start with 'isbn' or 'imdb'")
    return id

@app.get("/items")
def get_items(id:Annotated[str | None, AfterValidator(check_validation)] = None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))

    return {"id": id, "item": item}
