from fastapi import FastAPI, Depends
from . import models #import all our models
from .database import engine, get_db
from sqlalchemy.orm import Session #import to create a session in our api endpoint
from .routers import post, user, auth

app = FastAPI()


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

models.Base.metadata.create_all(bind=engine) #creates the tables once the application restarts(if table not already there) and if its already there it doesnt do anything, sqlalchemy is not capable of updating tables and data

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i


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

@app.get("/sqlalchemy") #test route 
async def test_posts(db: Session = Depends(get_db)): #creates a session to the database using the defined function
    posts = db.query(models.Post).all()
    return posts


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
