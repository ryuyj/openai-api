from fastapi import FastAPI
from routes import router

app = FastAPI()

# 라우터 등록
app.include_router(router)

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
