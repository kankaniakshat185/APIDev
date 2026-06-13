from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi import Body
from typing import List
from ..schemas import PostBase, PostCreate, PostResponse
from ..database import get_db
from sqlalchemy.orm.session import Session #import to create a session in our api endpoint
from .. import models, oauth2 #import all our models

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_posts(post: PostCreate, db: Session=Depends(get_db), user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", ("hey this is a new post", "this is content for the new post", "true")) #never pass values directly to prevent sql injections
    # new_post = cursor.fetchone() #using only psycopg driver
    # conn.commit() #using only psycopg driver-commit the changes to make them persistant
    new_post = models.Post(**post.dict()) #adding new post to database, use ** to unpack the dictionary
    db.add(new_post) #stage the changes
    db.commit() #commit the changes to make them persistant
    db.refresh(new_post) #refresh and add them back to the variable 
    print("Created and added new post")
    return new_post

@router.get("/{id}", response_model=PostResponse)
async def get_post(id: int, response: Response, db: Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id= %s """, (id,)) #using only psycopg driver
    #post=cursor.fetchone() #using only psycopg driver
    post=db.query(models.Post).filter(models.Post.id==id).first()
    #print(post)-gives you the raw sql command behind the above query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "requested resource not found"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session=Depends(get_db), user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"resource with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int, updated_post: PostCreate, db: Session=Depends(get_db), user: int=Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET (title, content, published) = (%s, %s, %s) WHERE id=%s RETURNING *""", (post.title, #post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"resource with id {id} not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
