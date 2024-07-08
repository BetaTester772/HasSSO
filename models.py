from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)

    key: str = Field(default=None)
    student_id: int = Field(default=None, unique=True)
    intranet_id: str = Field(default=None, unique=True)
    name: str = Field(default=None)


class Site(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(default=None)
    url: str = Field(default=None)
    description: str = Field(default=None)
    secret_key: str = Field(default=None)
