from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, article
from app.prisma import connect, disconnect

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4201"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)



@app.on_event("startup")
async def startup():
    await connect()

@app.on_event("shutdown")
async def shutdown():
    await disconnect()

app.include_router(auth.router, prefix="/api")
app.include_router(article.router, prefix="/api")
