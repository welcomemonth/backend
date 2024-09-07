from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserFormat(BaseModel):
    username: str
    email: EmailStr
    token: str
    bio: str
    image: str


class UserResponse(BaseModel):
    user: UserFormat

class UserLoginRequest(BaseModel):
    user: UserLogin

class UserCreateRequest(BaseModel):
    user: UserCreate