from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


#lets define the schema that we want from user ---- title - str, content - str

class Post(BaseModel):
    title:str  # field and type
    content:str
    published:bool = True #if user wants it to be published it or not default value is True
    rating:Optional[int] = None #rating from user but fully optional


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
def create_posts(payload:Post): 
    # body is good but issue is that user can send anything in request body or  payload and we are not able to validate it therefore we need to force client to send data in a schema that WE EXPECT!! Solution is -- PYDANTIC

    #pydantic will check if the payload has title and content or not -- and both are to be strings therefore it will do complete validation of data send by frontend
    print(payload.title) #we can extract data easily now
    print(payload.rating)

    print(payload.model_dump()) # each pydantic object has a inbuilt function called dict() but its deprecated now use model_dump()
    # return {
    #     "data":"new post"
    # }
    #now we can return payload
    return payload.model_dump()




