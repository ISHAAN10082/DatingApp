from typing import Union
from fastapi import FastAPI,Depends
from . import crud, models, schemas,database
from .database import engine, SessionLocal


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