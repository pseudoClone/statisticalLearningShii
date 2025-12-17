from fastapi import FastAPI

app = FastAPI()

@app.get("/user/me")
async def read_user_me():
    return {"user_id": "current_user"}

@app.get("/user/{user_id}")
async def read_user_with_id(user_id:str):
    return {"user_id": user_id}

# Donot ever redefine a path operation
