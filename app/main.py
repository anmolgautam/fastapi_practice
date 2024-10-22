from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional,List,Dict,Any
import json
from random import randrange
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

my_posts = [] 
my_posts.append({"title":"Favourite Pizza","content":"Maragarittaaaaaaa","id":1})
my_posts.append({"title":"Favourite Movie","content":"Matrixxxxx","id":2})


class Post(BaseModel):
    title:str  
    content:str
    published:bool = True 

 #otherwise the try and except and it will continue to start the server , which we shouldnot do
try:
    conn = psycopg2.connect(host="localhost",
                            database="fastapi_practice_database",
                            user="postgres",
                            password="root",
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DB connection Successful...")
except Exception as error:
    print("Connecting to DB failed : \n",error)
    time.sleep(3)



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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall() #fetchone is also there
    #print(posts)
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_posts(payload:Post): 
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (payload.title,payload.content,payload.published)
                   ) #dont do strinf manipulation using f"", use %s it saves us from SQL injection therefore use %s to sanitize the input
    new_post = cursor.fetchone()
    conn.commit()

    return {"data":new_post} 


@app.get("/posts/{id}") 
def get_post(id:int): 
    #print(id)
    cursor.execute("""SELECT * FROM posts WHERE id=(%s)""",(str(id),)) # this comma after str(id), is needed else the HTTP error is not processed somehow, weird !!! Figure out later why.
    post = cursor.fetchone()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return{"post_details":post} 


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post not found with id : {id}")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    #print(post)
    #index = find_post_index(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} not found")
    
    return {"data":updated_post}