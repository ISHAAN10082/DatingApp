from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from backend import models
import requests
import uuid
from geopy.distance import geodesic
from datetime import datetime




def fetch_and_store_users(db: Session, num_users: int):
    run_id = str(uuid.uuid4())  
    run_datetime = datetime.utcnow()
    users_to_add = []
    for i in range(num_users):
        try:
            response = requests.get("https://randomuser.me/api/")
            response.raise_for_status() 
            data = response.json()["results"][0]
        except requests.RequestException as e:
            print(f"An error occurred while fetching user data: {e}")
            continue  
        
        user = models.User(
            uid=data["login"]["uuid"],
            email=data["email"],
            first_name=data["name"]["first"],
            last_name=data["name"]["last"],
            gender=data["gender"],
            latitude=float(data["location"]["coordinates"]["latitude"]),
            longitude=float(data["location"]["coordinates"]["longitude"]),
            run_id=run_id,
            run_iteration=i + 1,  
            datetime=run_datetime
        )
        users_to_add.append(user)
    
    db.add_all(users_to_add)
    db.commit()
    
    total_users = db.query(models.User).count()
    return {"message": f"Added {len(users_to_add)} new users. Total users: {total_users}", "run_id": run_id}
    

def get_random_user(db: Session):
    return db.query(models.User).order_by(func.random()).first()


def get_random_username(db: Session):
    random_user = get_random_user(db)
    if random_user:
        return f"{random_user.first_name} {random_user.last_name}"
    return None


def get_nearest_users(db: Session, email: str, x: int):
    user = db.query(models.User).filter(models.User.email== email).first()
    if not user:
        return []
    
    all_users = db.query(models.User).all()
    distances = []
    for other_user in all_users:
        if other_user.email != user.email:
            distance = geodesic((user.latitude, user.longitude), (other_user.latitude, other_user.longitude)).miles
            distances.append((other_user, distance))
    
    distances.sort(key=lambda x: x[1])
    return [u[0] for u in distances[:x]]

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def update_user_location(db: Session, email: str, latitude: float, longitude: float):
    user = get_user_by_email(db, email)
    if user:
        user.latitude = latitude
        user.longitude = longitude
        db.commit()
        return user
    return None

def get_user_by_uid(db: Session, uid: str):
    return db.query(models.User).filter(models.User.uid == uid).first()

def delete_user(db: Session, uid: str):
    user = get_user_by_uid(db, uid)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

