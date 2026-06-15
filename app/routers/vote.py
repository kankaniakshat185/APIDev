from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm.session import Session


router = APIRouter(
    prefix = "/vote",
    tags= ["Votes"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post.id).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.posts_id==models.Post.id, models.Vote.users_id==models.User.id)
    found_vote = vote_query.first()

    if (vote.dir)==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post with id {vote.post_id}")
        else:
            new_vote = models.Vote(posts_id=vote.post_id, users_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message: Succesfull vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote on post with id {vote.posts_id} does not exist via user {current_user.id}")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"Message: Succesfully deleted vote!"}


