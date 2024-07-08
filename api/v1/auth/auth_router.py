from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from starlette.config import Config
import hashlib
from sqlmodel import select
from models import User
import datetime
import jwt
import os
from api.v1.auth.auth_crude import get_secret_key
from fastapi_utils.tasks import repeat_every

config = Config('.env')
SALT = config.get('SALT')

ALGORITHM = "HS256"

router = APIRouter(prefix="/api/v1/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

#
# class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
#     def __init__(self, grant_type: str = None, intranet_id: str = None, intranet_pw: str = None,
#                  scope: str = "", client_id: Optional[str] = None,
#                  client_secret: Optional[str] = None, url: Optional[str] = None):
#         self.url = url
#         super().__init__(grant_type=grant_type, username=intranet_id, password=intranet_pw,
#                          scope=scope, client_id=client_id, client_secret=client_secret)
#
#

auth_temporary_dict = {
        # "temp_token": {"site": "site", "student_name": "name", "student_id": "student_id"},
        "asdf": {"site"  : "search", "student_name": "홍길동", "student_id": "10",
                 "expire": datetime.datetime(2024, 7, 8, 0, 0, 0)},
}


def remove_expired_token():
    global auth_temporary_dict
    key_to_remove = []
    for key, value in auth_temporary_dict.items():
        if value["expire"] < datetime.datetime.now():
            key_to_remove.append(key)

    for key in key_to_remove:
        try:
            auth_temporary_dict.pop(key)
        except KeyError:
            pass


@router.post("/token")
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    form_data = {
            "site"      : form_data.username,
            "temp_token": form_data.password
    }

    if auth_temporary_dict.get(form_data["temp_token"]) is None or auth_temporary_dict[form_data["temp_token"]][
        "site"] != form_data["site"] or auth_temporary_dict[form_data["temp_token"]][
        "expire"] < datetime.datetime.now():
        remove_expired_token()  # 몰래 하기
        raise HTTPException(status_code=403, detail='인증되지 않은 토큰입니다.')

    student_id = auth_temporary_dict[form_data["temp_token"]]["student_id"]
    student_name = auth_temporary_dict[form_data["temp_token"]]["student_name"]
    secret_key = get_secret_key(db, form_data["site"])

    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"student_id": student_id, "student_name": student_name, "exp": expiration}, secret_key,
                       algorithm="HS256")

    auth_temporary_dict.pop(form_data["temp_token"])

    return {"access_token": token, "token_type": "bearer"}


class Verify(BaseModel):
    intranet_id: str
    intranet_pw: str
    site_url: str


@router.post("/verify")
def verify_student(verify: Verify, db: Session = Depends(get_session)):
    _ = get_secret_key(db, verify.site_url)
    input_hashed_key = hashlib.sha256((verify.intranet_id + verify.intranet_pw + SALT).encode()).hexdigest()

    statement = select(User).where(User.key == input_hashed_key)
    results = db.exec(statement)

    user = results.first()

    if user is None:
        raise HTTPException(status_code=403, detail='인트라넷 아이디와 비밀번호가 일치하지 않습니다')

    temp_token = os.urandom(15).hex()

    auth_temporary_dict[temp_token] = {"site"      : verify.site_url, "student_name": user.name,
                                       "student_id": user.student_id,
                                       "expire"    : datetime.datetime.now() + datetime.timedelta(minutes=5)}

    return {"temp_token": temp_token}
