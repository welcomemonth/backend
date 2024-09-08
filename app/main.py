from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.routes import auth, article, prd
from app.sql.database import Base, engine
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4201"],  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "11206"
    correct_password = "123456abc"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/openapi.json", dependencies=[Depends(verify_credentials)])
async def get_open_api_endpoint():
    return get_openapi(title="openapi", version="1.0.0", routes=app.routes)

@app.get("/docs", dependencies=[Depends(verify_credentials)])
async def get_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/redoc", dependencies=[Depends(verify_credentials)])
async def get_redoc():
    return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")

app.include_router(auth.router, prefix="/api")
app.include_router(article.router, prefix="/api")
app.include_router(prd.router, prefix="/api")
