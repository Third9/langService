from fastapi import FastAPI
from dotenv import load_dotenv

# 환경 변수 먼저 로드
load_dotenv()

from src.api.search import router as search_router

app = FastAPI()

# 라우터 등록
app.include_router(search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)