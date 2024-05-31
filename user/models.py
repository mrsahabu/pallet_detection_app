from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from core.database import Base
from sqlalchemy.sql.sqltypes import Float as SQLAlchemyFloat


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(512))
    role = Column(String(50))

    class Config:
        orm_mode = True


class DataModel(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pallets_count = Column(Integer)
    insert_time = Column(DateTime, default=datetime.utcnow)
    price_piece = Column(Float)
    total_price = Column(Float)
    transport_fc_count = Column(Float)
    co2_saving_count = Column(Float)
    total_transport = Column(Float)
    co2_fc = Column(Float)
    transport_cost = Column(Float)
    buy_or_sell = Column(String(255))

    files = relationship("FileModel", back_populates="data")

    class Config:
        orm_mode = True

class FileModel(Base):
    __tablename__ = "image_data"
    id = Column(Integer, primary_key=True, index=True)
    data_id = Column(Integer, ForeignKey('user_data.id'))  # Foreign key to DataModel
    img_path = Column(String(255))

    # Define relationship to DataModel
    data = relationship("DataModel", back_populates="files")

    class Config:
        orm_mode = True

    

# Map SQLAlchemy Float type to Pydantic float type
DataModel.__annotations__["price_piece"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["total_price"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["transport_fc_count"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["co2_saving_count"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["total_transport"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["co2_fc"] = (float, SQLAlchemyFloat)
DataModel.__annotations__["transport_cost"] = (float, SQLAlchemyFloat)