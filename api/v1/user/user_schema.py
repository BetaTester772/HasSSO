from pydantic import BaseModel


class UserCreate(BaseModel):
    intranet_id: str
    intranet_pw: str
