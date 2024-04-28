from app import schemas, utils
from app.database import get_db
from app import oauth2
from app import models

from sqlalchemy.orm import Session

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends

#pydantic things
from typing import  List #list is used to define a response model that return a list


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserResponse]) #List say that the response is a list of that PostResponse Class
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get all the users (users table rows)

    Returns:
        list[dict]: all the users dictionary
    """    
    if current_user.role != "administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Need privileged access to get this data. your role: {current_user.role}")
    users = db.query(models.Users).all()
    return users


@router.get("/identity", response_model=schemas.UserResponse) #List say that the response is a list of that PostResponse Class
def get_current_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get the current logged user based on bearer token
    Returns:
        dict: current user dictionary
    """    
    current_user = db.query(models.Users).filter(models.Users.email == current_user.email).first()
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists")
    
    #hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    
    # cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *',
    #                 (user.email, user.password))
    # new_user = cursor.fetchone()    # fetchone is needed if I check the response_model
    # conn.commit()                   # this commit the change
    
    new_user = models.Users(email=user.email, password=user.password, name=user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # this return * the newly committed value

    return new_user


@router.get("/id/{id}", response_model=schemas.UserResponse)
def get_user_info_from_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """if administrator, retrive user non-sensitive data by id

    Args:
        id (int): id

    Raises:
        HTTPException: Id doesn't exists

    Returns:
        user: class UserResponse(BaseModel):
                created_at: datetime
                email: EmailStr
                name: str
                id: int
                role: str
    """    
    # cursor.execute(f'SELECT * FROM users WHERE id = {id}')
    # user = cursor.fetchone()
    if current_user.role != "administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Need privileged access to get this data. your role: {current_user.role}")
    
    user = db.query(models.Users).where(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} does not exist')

    return user


@router.get("/email/{email}", response_model=schemas.UserResponse)
def get_user_info_from_email(email: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """if administrator, retrive user non-sensitive data by email

    Args:
        email (int): email

    Raises:
        HTTPException: email doesn't exists

    Returns:
        user: class UserResponse(BaseModel):
                created_at: datetime
                email: EmailStr
                name: str
                id: int
                role: str
    """   
    # cursor.execute(f'SELECT * FROM users WHERE id = {id}')
    # user = cursor.fetchone()
    if current_user.role != "administrator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Need privileged access to get this data. your role: {current_user.role}")
    
    user = db.query(models.Users).where(models.Users.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with email {email} does not exist')

    return user



