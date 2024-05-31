from pydantic import BaseModel, EmailStr
from typing import Union
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey, Float


class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    idusers: int
    username: str
    email: EmailStr


class ImageSchema(BaseModel):
    id: int
    user_id: int
    img_path: str
    pallets_count: Optional[int]
    insert_time: datetime
    price_piece: Float
    total_price: Float
    transport_fc_count: Float
    co2_saving_count: Float
    total_transport: Float
    co2_fc: Float
    transport_cost: Float
    buy_or_sell: String

    class Config:
        arbitrary_types_allowed = True
