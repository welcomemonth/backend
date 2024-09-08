from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.jwt import create_access_token, verify_token
from app.sql.schemas.user import UserResponse, UserCreateRequest, UserLoginRequest, UserFormat
from app.sql.models.user import User
from app.services.auth import hash_password, verify_password
from app.sql.crud.user import get_user_by_email, get_user_by_username
from app.sql.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    user = request.user
    existing_user_by_email = get_user_by_email(db=db, email=user.email)
    existing_user_by_username = get_user_by_username(db=db, username=user.username)

    if existing_user_by_email or existing_user_by_username:
        errors = {}
        if existing_user_by_email:
            errors["email"] = ["has already been taken"]
        if existing_user_by_username:
            errors["username"] = ["has already been taken"]
        print("已存在信息：", errors)
        raise HTTPException(status_code=422, detail={"errors": errors})
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password)
    success_save_user = new_user.save(db)
    return_userinfo = UserFormat(
        username=success_save_user.username,
        email=success_save_user.email,
        token=create_access_token(data={"sub": success_save_user.username}),
        bio=success_save_user.bio if success_save_user.bio else "",
        image=success_save_user.image
    )
    return UserResponse(user=return_userinfo)


@router.post("/users/login", response_model=UserResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    user = request.user
    db_user: User = get_user_by_email(db=db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=422, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username})
    userinfo = UserFormat(
        username=db_user.username,
        email=db_user.email,
        token=token,
        bio=db_user.bio if db_user.bio else "",
        image=db_user.image
        )
    return UserResponse(user=userinfo)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 验证用户名和密码
    db_user = get_user_by_username(form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # 创建访问 token
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user", response_model=UserResponse)
async def get_user(user:User = Depends(get_current_user)):
    userinfo = UserFormat(
        username=user.username,
        email=user.email,
        token=create_access_token(data={"sub": user.username}),
        bio=user.bio if user.bio else "",
        image=user.image
    )
    return UserResponse(user=userinfo)


@router.get("/profiles/{username}", response_model=UserResponse)
async def get_profile(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    userinfo = UserFormat(
        username=user.username,
        email=user.email,
        token=create_access_token(data={"sub": user.username}),
        bio=user.bio if user.bio else "",
        image=user.image
    )
    return UserResponse(user=userinfo)

