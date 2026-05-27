from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, models, schemas, utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login")
async def user_login(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_auth.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credentials Invalid")
    
    if not utils.verify(user_auth.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Credentials Invalid")
    
    created_token = oauth2.create_access_token({"user_info": user.id})
    #created token
    #send user token
    return {"Created token" : created_token, "token_type" :  "bearer"}
    