from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional,List,Dict,Any
import json
from random import randrange

app = FastAPI()

#------------CRUD------------#
#standard convention for api -- use plurals, like posts, users
#use an identifier in db to get, delete, patch or put a post
#put ---> pass all the information for updating few or all the info
#patch ----> send only the necessary field that is to be updated ---- will not be using this now


#lets start saving posts in memory using a global var
my_posts = [] 
my_posts.append({"title":"Favourite Pizza","content":"Maragarittaaaaaaa","id":1})
my_posts.append({"title":"Favourite Movie","content":"Matrixxxxx","id":2})


class Post(BaseModel):
    title:str  
    content:str
    published:bool = True 
    rating:Optional[int] = None 


@app.get("/")
def home():
    return {
        "message":"Welcome to the matrix..."
    }

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts") #update the naming for createposts to posts
def create_posts(payload:Post): 
    post_dict = payload.model_dump()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data":payload.model_dump()} #generally when post request is created it should respond with the data




