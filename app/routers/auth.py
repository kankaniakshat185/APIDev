from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, utils, oauth2, schemas


router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
async def user_login(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_auth.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials Invalid")
    
    if not utils.verify(user_auth.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials Invalid")
    
    created_token = oauth2.create_access_token({"user_id": user.id})
    #created token
    #send user token
    return {"access_token" : created_token, "token_type" :  "bearer"}
    