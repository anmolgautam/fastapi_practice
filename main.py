from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"Welcome to the matrix..."
    }

@app.get("/posts")
def get_posts():
    return {
        "data":"This is your new post"
    }

@app.post("/createposts")
def create_posts(payload:dict = Body(...)): #Body works but we need to 
    print(payload)
    return {
        "new post":f"title is {payload['title']}"
    }


