from typing import Union
from fastapi import FastAPI,Depends, HTTPException
from . import crud, models, schemas
from .database import engine, SessionLocal
from requests import  Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/fetch_users/", response_model=schemas.Message)
async def fetch_users(num_users: int, db: Session = Depends(get_db)):
    return crud.fetch_and_store_users(db, num_users)


@app.get("/random_user/", response_model=schemas.User)
async def get_random_user(db: Session = Depends(get_db)):
    return crud.get_random_user(db)


@app.get("/nearest_users/", response_model=list[schemas.User])
async def get_nearest_users(uid: str, x: int, db: Session = Depends(get_db)):
    return crud.get_nearest_users(db, uid, x)


@app.get("/random_username/", response_model=str)
async def get_random_username(db: Session = Depends(get_db)):
    username = crud.get_random_username(db)
    if username:
        return username
    raise HTTPException(status_code=404, detail="No users found in the database")