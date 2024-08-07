from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from . import models
import requests
import random
from geopy.distance import geodesic


def fetch_and_store_users(db: Session, num_users: int):
    run_id = random.randint(1, 1000000)
    for _ in range(num_users):
        response = requests.get("https://randomuser.me/api/")
        data = response.json()["results"][0]
        
        user = models.User(
            uid=data["login"]["uuid"],
            email=data["email"],
            first_name=data["name"]["first"],
            last_name=data["name"]["last"],
            gender=data["gender"],
            latitude=float(data["location"]["coordinates"]["latitude"]),
            longitude=float(data["location"]["coordinates"]["longitude"]),
            run_id=run_id
        )
        db.add(user)
    
    db.commit()
    return {"message": f"Added {num_users} users"}

def get_random_user(db: Session):
    return db.query(models.User).order_by(func.random()).first()

def get_nearest_users(db: Session, uid: str, x: int):
    user = db.query(models.User).filter(models.User.uid == uid).first()
    if not user:
        return []
    
    all_users = db.query(models.User).all()
    distances = []
    for other_user in all_users:
        if other_user.uid != user.uid:
            distance = geodesic((user.latitude, user.longitude), (other_user.latitude, other_user.longitude)).miles
            distances.append((other_user, distance))
    
    distances.sort(key=lambda x: x[1])
    return [u[0] for u in distances[:x]]