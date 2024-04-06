from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello World"}

@app.get("/posts")
def post():
    return {"data": "frist post"}

@app.post("/createposts")
def create_post():
    return {"messge": "created successfully"}