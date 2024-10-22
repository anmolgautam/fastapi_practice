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

def find_post(id):
    for post in my_posts:
        if post["id"]==id: #can remove int(id) here to id as we are forcing validation at request level
            return post

@app.get("/")
def home():
    return {
        "message":"Welcome to the matrix..."
    }

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED) #update the naming for createposts to posts
def create_posts(payload:Post): #set up a status code here as well based on mdn docs if an entity is created send a response 201 in router
    post_dict = payload.model_dump()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data":payload.model_dump()} #generally when post request is created it should respond with the data


@app.get("/posts/{id}") #id here is path parameter, fastapi automatically parses the id so we can pass it to the function directly
def get_post(id:int): #we want id to be integer thereby forcing validation
    print(id)
    # for post in my_posts:
    #     if post["id"]==int(id):
    #         return {"post_detail":post}
    # since finding a post based on id can be separated out as a separate logic so lets create a method/function for it and call it here

    #if suppose a id doesnt exist instead of returning not found return valid HTTP exceptions, so frontend gets proper info - 404 error - item not found or resource doesn't exist 
    post = find_post(id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND #we can use status object from fastapi to set it up instead of manually setting response.status_code = 404
        #return {"post_details":f"Post with {id} not found"} # but its not fol proof raise a HTTP exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    
    return{"post_details":post} 

#IMP ------ if we create anopther route like "/posts/latest" to get the latest post then it will go to /posts/{id} and will give validation error therefore ordering of API routes are important.
