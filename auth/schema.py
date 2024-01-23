from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password1: str
    password2: str


class User_In_Db(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    balance: float


class User_Info(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    balance: float



