from app import schemas
from app.database import get_db
from app import oauth2
from app import models

from sqlalchemy.orm import Session

from datetime import datetime

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
    """Get all todo for current user 

    Returns:
        list[dict]: all the user's todos
    """    
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()
    return todos


@router.get("/bydate", response_model=List[schemas.TodoResponse])
def get_todo_by_date(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
             start: datetime = datetime.now(), 
             end: Optional[datetime] = None):
    """Get all todo for current user filtered by dueDate

    **if no starting date is provided, the actual time is used 

    Returns:
        list[dict]: all the user's todos filtered by dueDate
    """    
    if start:
        if end:
            print(start, end)
            filtered_todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id, models.Todo.dueDate >= start, models.Todo.dueDate <= end).all()
        else:
            filtered_todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id, models.Todo.dueDate >= start).all()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"no start date or end date provided")
 
    return filtered_todos


@router.get("/bycontent", response_model=List[schemas.TodoResponse])
def get_todo_by_content(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
             contains: str = ""):
    """Get all todo for current user filtered by content (case insentitive)
    the query parameter "contains" will be searched as a substring inside the "text" column of todos

    Returns:
        list[dict]: all the user's todos filtered by content
    """    
    filtered_todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id, models.Todo.text.icontains(contains)).all()
 
    return filtered_todos

    


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoResponse)
def create_data(data: schemas.TodoCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    try:
        print(dict(data))
        # Create new todo. no duplicate check since duplicate ARE allowed. handle dueDate optionality
        if data.dueDate is not None:
            new_data = models.Todo(text=data.text, dueDate=data.dueDate, owner_id=current_user.id)
        else:
            new_data = models.Todo(text=data.text, owner_id=current_user.id)

        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data

    except Exception as e:
        db.rollback()  # Ensure the session is rolled back in case of any other exceptions
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



@router.put("/update/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db), 
                          current_user: int = Depends(oauth2.get_current_user)):
    """Update a todo    
    
    Args:
        todo_id (int): The ID of the todo to update.
        todo_update (schemas.TodoUpdate): The new values for the todo.
    
    Returns:
        schemas.TodoResponse: The updated todo.
    """
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found or not owned by the user")
    
    if todo_update.text is not None:
        todo.text = todo_update.text
    if todo_update.important is not None:
        todo.important = todo_update.important
    if todo_update.done is not None:
        todo.done = todo_update.done
    if todo_update.dueDate is not None:
        todo.dueDate = todo_update.dueDate

    db.commit()
    db.refresh(todo)
    
    return todo



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


