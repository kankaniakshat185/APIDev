from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..utils import Hash
from ..schemas import UserCreate, UserResponse
from ..database import get_db
from .. import models #import all our models
from sqlalchemy.orm.session import Session #import to create a session in our api endpoint

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: Session=Depends(get_db)):

    user.password = Hash(user.password)

    new_user = models.User(**user.dict()) #adding new user to database, use ** to unpack the dictionary
    db.add(new_user) #stage the changes
    db.commit() #commit the changes to make them persistant
    db.refresh(new_user) #refresh and add them back to the variable 
    print("Created and added new user")
    return new_user


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db:Session=Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id==id).first() 

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
    
    return user