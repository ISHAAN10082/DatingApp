import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# print("Python path in main.py:", sys.path)
# print("Current directory in main.py:", __file__)

# try:
#     from . import crud, models, schemas
#     print("crud, models, and schemas imported successfully")
# except ImportError as e:
#     print(f"Failed to import crud, models, or schemas: {e}")

# try:
#     from .database import engine, SessionLocal
#     print("database imported successfully")
# except ImportError as e:
#     print(f"Failed to import database: {e}")

# Rest of your main.py code...

from database import SessionLocal, engine

from typing import Union
from fastapi import FastAPI,Depends, HTTPException
from backend import crud, models, schemas
# from database import engine, SessionLocal
from requests import  Session

#models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependency function in FastAPI that provides a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db  #returns the session to the caller
    finally:
        db.close()



@app.post("/fetch_users/", response_model=schemas.Message)
async def fetch_users(num_users: int, db: Session = Depends(get_db)):
    return crud.fetch_and_store_users(db, num_users)


@app.get("/random_user/", response_model=schemas.User)
async def get_random_user(db: Session = Depends(get_db)):
    user = crud.get_random_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="No users found in the database")
    
    # Add a log message
    print(f"Random user retrieved: {user.first_name} {user.last_name}")
    
    # Convert the user object to a dictionary and add a custom field
    user_dict = schemas.User.from_orm(user).dict()
    user_dict["full_name"] = f"{user.first_name} {user.last_name}"
    
    return user_dict


@app.get("/nearest_users/", response_model=list[schemas.User])
async def get_nearest_users(email: str, x: int, db: Session = Depends(get_db)):
    users = crud.get_nearest_users(db, email, x)
    if not users:
        raise HTTPException(status_code=404, detail="User not found / no nearby users")
    return users


@app.get("/random_username/", response_model=str)
async def get_random_username(db: Session = Depends(get_db)):
    username = crud.get_random_username(db)
    if not username:
        raise HTTPException(status_code=404, detail="No users found in the database")
    return username + "!"

@app.get("/user_count/", response_model=int)
async def get_user_count(db: Session = Depends(get_db)):
    count = crud.get_user_count(db)
    return count
