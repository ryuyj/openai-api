from pydantic import BaseModel

# 질문 요청을 위한 모델
class Query(BaseModel):
    question: str
