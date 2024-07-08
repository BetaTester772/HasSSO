from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id = Field(default=None, primary_key=True, index=True)

    key = Field(default=None)
    student_id = Field(default=None)
