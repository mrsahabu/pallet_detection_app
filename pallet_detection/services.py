from datetime import datetime

from user.models import UserModel, ImgsModel
from sqlalchemy.orm import Session


async def insert_img(
    db: Session,
    img_path: str,
    user_id: int,
    pallets_count: int,
    insert_time: datetime,
    price_piece: float,
    total_price: float,
    transport_fc_count: float,
    co2_saving_count: float,
    total_transport: float,
    co2_fc: float,
    transport_cost: float,
    buy_or_sell: str
):
    try:
        img_insert = ImgsModel(
            img_path=img_path,
            user_id=user_id,
            pallets_count=pallets_count,
            insert_time=insert_time,
            price_piece=price_piece,
            total_price=total_price,
            transport_fc_count=transport_fc_count,
            co2_saving_count=co2_saving_count,
            total_transport=total_transport,
            co2_fc=co2_fc,
            transport_cost=transport_cost,
            buy_or_sell=buy_or_sell
        )
        db.add(img_insert)
        db.commit()
        db.refresh(img_insert)
    except Exception as e:
        raise e
        return False
    return True

