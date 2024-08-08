from typing import Union
from fastapi import FastAPI,Depends, HTTPException
import crud, models, schemas
from database import engine, SessionLocal
from requests import  Session

models.Base.metadata.drop_all(bind=engine)
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
        raise HTTPException(status_code=404, detail="No users found")
    return user


@app.get("/nearest_users/", response_model=list[schemas.User])
async def get_nearest_users(uid: str, x: int, db: Session = Depends(get_db)):
    users = crud.get_nearest_users(db, uid, x)
    if not users:
        raise HTTPException(status_code=404, detail="User not found / no nearby users")
    return users


@app.get("/random_username/", response_model=str)
async def get_random_username(db: Session = Depends(get_db)):
    username = crud.get_random_username(db)
    if not username:
       raise HTTPException(status_code=404, detail="No users found in the database")
    return username
    