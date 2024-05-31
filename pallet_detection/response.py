from pydantic import BaseModel
from datetime import datetime
from typing import List

class FileModelResponse(BaseModel):
    id: int
    img_path: str

    class Config:
        orm_mode = True

class DataModelResponse(BaseModel):
    data_id: int
    user_id: int
    pallets_count: int
    insert_time: datetime
    price_piece: float
    total_price: float
    transport_fc_count: float
    co2_saving_count: float
    total_transport: float
    co2_fc: float
    transport_cost: float
    buy_or_sell: str
    files: List[FileModelResponse]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
