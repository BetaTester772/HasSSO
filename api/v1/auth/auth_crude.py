# crud
from sqlalchemy.orm import Session
from api.v1.user.user_schema import UserCreate
from models import Site
from api.v1.tool.intranet import approve_and_get_id_name
from fastapi import HTTPException
import hashlib
from sqlmodel import select

from starlette.config import Config

config = Config('.env')
SALT = config.get('SALT')


def get_secret_key(db: Session,
                   site_url: str,
                   ):
    statement = select(Site).where(Site.url == site_url)
    result = db.exec(statement).first()

    if result is None:
        raise HTTPException(status_code=404, detail='사이트 정보가 없습니다.')

    return result.secret_key
