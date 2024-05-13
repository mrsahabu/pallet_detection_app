from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    idusers = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(512))


class ImgsModel(Base):
    __tablename__ = "user_videos"
    iduser_img = Column(Integer, primary_key=True, index=True)
    img_path = Column(String())
    user_id = Column(Integer, ForeignKey('users.idusers'))
    pallets_count = Column(Integer)
    insert_time = Column(DateTime, default=datetime.utcnow)