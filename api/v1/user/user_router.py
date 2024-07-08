from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from api.v1.user.user_schema import UserCreate
from api.v1.user.user_crud import add_user, update_user, get_user

from api.v1.auth.auth_router import oauth2_scheme

router = APIRouter(prefix="/api/v1/user")


@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    if get_user(db, user.intranet_id) is not None:
        raise HTTPException(status_code=409, detail='이미 가입된 사용자입니다.')
    add_user(db, user)
    return {"message": "회원가입이 완료되었습니다."}


@router.post("/update")
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    update_user(db, user)
    return {"message": "정보 수정이 완료되었습니다."}

# def get_current_user(token: str = Depends(oauth2_scheme),
#                      db: Session = Depends(get_session)):
#     credentials_exception = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     else:
#         user = get_user(db, intranet_id=username)
#         if user is None:
#             raise credentials_exception
#         return user
