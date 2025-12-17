from fastapi import FastAPI

app = FastAPI()

@app.get("/{file_path:path}")
async def get_file(file_path:str):
    return {"file_path": file_path}

