from passlib.context import CryptContext
from app.prisma import prisma

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = prisma.user.find_first(where={"username": username})
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
