from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models #import all our models
from sqlalchemy.orm import Session #import to create a session in our api endpoint
from.database import engine, get_db

models.Base.metadata.create_all(bind=engine) #creates the tables once the application restarts(if table not already there) and if its already there it doesnt do anything, sqlalchemy is not capable of updating tables and data




app = FastAPI()

while True:  #to continue trying to connect to the databse until successful

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='@k$#@!04',cursor_factory=RealDictCursor) #establishing a connection to the database
        cursor = conn.cursor()  #cursor is used to execute the commands
        print("Database connection was succesfull!!")
        break

    except Exception as error:
        print("Connecting to databse failed")    #except the error if connection failed
        print("Error: ", error)
        time.sleep(3)
 


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]=None


@app.get("/")
async def root():
    return {"message": "Hello Akshat"}

#[ Your Python Code ] 
#       │
#       ▼ (Generates abstract SQL query)
#[ SQLAlchemy Engine ] 
#       │
#       ▼ (Passes SQL string and parameters)
#[ psycopg2 Driver ] 
#       │
#       ▼ (Sends query over network)
#[ PostgreSQL Database ]

#so we use sqlalchemy to abstractly create sql queies which are then run using psycopg (database driver)

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)): #creates a session to the database using the defined function
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
async def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", ("hey this is a new post", "this is content for the new post", "true")) #never pass values directly to prevent sql injections
    # new_post = cursor.fetchone() #using only psycopg driver
    # conn.commit() #using only psycopg driver-commit the changes to make them persistant
    new_post = models.Post(**post.dict()) #adding new post to database, use ** to unpack the dictionary
    db.add(new_post) #stage the changes
    db.commit() #commit the changes to make them persistant
    db.refresh(new_post) #refresh and add them back to the variable 
    print("Created and added new post")
    return {"data": new_post}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response, db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id= %s """, (id,)) #using only psycopg driver
    #post=cursor.fetchone() #using only psycopg driver
    post=db.query(models.Post).filter(models.Post.id==id).first()
    #print(post)-gives you the raw sql command behind thee above query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "requested resource not found"}
    return {"data": post}


@app.delete("/posts/{id}")
async def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"resource with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id=%s RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"resource with id {id} not found")
    return {"data": updated_post}