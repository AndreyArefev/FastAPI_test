from pydantic import BaseModel, constr, EmailStr
from typing import List, Optional
from .accounts import Account



class BaseUser(BaseModel):
    email: EmailStr
    username: constr(max_length=120)

    class Config:
        orm_mode = True


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    user_id: int
    is_active: bool = 'False'
    is_superuser: str = 'user'


class UserAccounts(User):
    accounts: List[Account]


class UserStatus(BaseModel):
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class EmailSchema(BaseModel):
    email: List[EmailStr]