# crud
from sqlalchemy.orm import Session
from api.v1.user.user_schema import UserCreate
from models import User
from api.v1.tool.intranet import approve_and_get_id_name
from fastapi import HTTPException
import hashlib
from sqlmodel import select

from starlette.config import Config

config = Config('.env')
SALT = config.get('SALT')


def add_user(db: Session, user: UserCreate):
    student_id, student_name = approve_and_get_id_name(user.intranet_id, user.intranet_pw)
    if student_id is None or student_id is None:
        raise HTTPException(status_code=403, detail='인트라넷 아이디와 비밀번호가 일치하지 않습니다')

    # make hashed_key with intranet_id, intranet_pw, and SALT
    hashed_key = hashlib.sha256((user.intranet_id + user.intranet_pw + SALT).encode()).hexdigest()

    new_user = User(
            name=student_name,
            student_id=student_id,
            key=hashed_key,
            intranet_id=user.intranet_id
    )

    db.add(new_user)

    db.commit()


def update_user(db: Session, user_data: UserCreate):
    student_id, student_name = approve_and_get_id_name(user_data.intranet_id, user_data.intranet_pw)
    if student_id is None or student_name is None:
        raise HTTPException(status_code=403, detail='인트라넷 아이디와 비밀번호가 일치하지 않습니다')

    statement = select(User).where(User.student_id == student_id)
    user = db.exec(statement).one()
    user.key = hashlib.sha256((user_data.intranet_id + user_data.intranet_pw + SALT).encode()).hexdigest()
    user.name = student_name
    user.intranet_id = user_data.intranet_id
    db.add(user)
    db.commit()


def get_user(db: Session,
             intranet_id: str,
             ):

    statement = select(User).where(User.intranet_id == intranet_id)
    results = db.exec(statement)

    # if len(results) > 0:
    user = results.first()
    return user
    # else:
    #     return None
