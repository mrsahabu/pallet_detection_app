from user.models import UserModel, ImgsModel
from sqlalchemy.orm import Session


async def insert_img(db: Session, img_path, user_id, pallets_count, insert_time):
    try:
        img_insert = ImgsModel(
            img_path=img_path,
            user_id=user_id,
            pallets_count=pallets_count,
            insert_time=insert_time
        )
        db.add(img_insert)
        db.commit()
        db.refresh(img_insert)
    except Exception as e:
        raise e
        return False
    return True
