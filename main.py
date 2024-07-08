from fastapi import FastAPI
from database import conn
from fastapi.middleware.cors import CORSMiddleware

# FastAPI
app = FastAPI()

# CORS middleware
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

# 라우터 추가 with list
from api.v1.user import user_router
from api.v1.auth import auth_router

app.include_router(user_router.router)
app.include_router(auth_router.router)


# 애플리케이션이 시작 될 때 데이터베이스를 생성하도록 만듬
@app.on_event("startup")
def on_startup():
    conn()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
