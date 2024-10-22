from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional,List,Dict,Any
import json
from random import randrange
from fastapi import Response
from fastapi import status
from fastapi import HTTPException

app = FastAPI()

my_posts = [] 
my_posts.append({"title":"Favourite Pizza","content":"Maragarittaaaaaaa","id":1})
my_posts.append({"title":"Favourite Movie","content":"Matrixxxxx","id":2})


class Post(BaseModel):
    title:str  
    content:str
    published:bool = True 
    rating:Optional[int] = None 

def find_post(id):
    for post in my_posts:
        if post["id"]==id: 
            return post
        
def find_post_index(id):
    for idx,p in enumerate(my_posts):
        if p["id"] == id:
            return idx

@app.get("/")
def home():
    return {
        "message":"Welcome to the matrix..."
    }

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_posts(payload:Post): 
    post_dict = payload.model_dump()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data":payload.model_dump()} 


@app.get("/posts/{id}") 
def get_post(id:int): 
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return{"post_details":post} 


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id : {id}")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    print(post)
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data":post_dict}