from app import schemas, utils
from app.database import get_db
from app import oauth2
from app import models

from sqlalchemy.orm import Session

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.exc import IntegrityError

#pydantic things
from typing import  List #list is used to define a response model that return a list


router = APIRouter(
    prefix="/todo",
    tags=['Todo']
)


@router.get("/", response_model=List[schemas.TodoResponse])
def get_data(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """Get all the todo for that user 

    Returns:
        list[dict]: all the user's inventories
    """    
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()
    return todos

    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoResponse)
def create_data(data: schemas.TodoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    try:
        # Create new todo. no duplicate check since duplicate ARE allowed
        new_data = models.Todo(text=data.text, dueDate=data.dueDate, owner_id=current_user.id)
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data

    except Exception as e:
        db.rollback()  # Ensure the session is rolled back in case of any other exceptions
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



@router.delete("/{id}")
def delete_data(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if id != None:
        #This query is reduntant since Todo.id filtering is enough, but is more robust 
        todo = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id, models.Todo.id == id).first() 
        if todo is None:
            raise HTTPException(status_code=404, detail=f"Todo with id: {id} not found for used {current_user.email}")
        else:
            # If data exists, delete it
            db.delete(todo)
            db.commit()
    else:
        raise HTTPException(status_code=404, detail="No id has been passed")
    
    return {"message": f"todo with id {id} correctly deleted"}


