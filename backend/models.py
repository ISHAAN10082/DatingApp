from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    #id = Column(Integer, primary_key=True, index=True) 
    uid = Column(String, unique=True,primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    run_id = Column(String, index=True)  
    run_iteration = Column(Integer)  
    datetime = Column(DateTime, default=datetime.utcnow)