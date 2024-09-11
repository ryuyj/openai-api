from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv  # 환경 변수를 로드하는 dotenv 라이브러리의 load_dotenv 함수를 임포트합니다.
import os                      # 환경 변수에 접근하기 위해 os 모듈을 임포트합니다.

# .env 파일에서 환경 변수를 로드합니다. 이 파일에 API 키와 같은 중요한 설정 정보를 저장할 수 있습니다.
load_dotenv()

# OpenAI 클라이언트 설정
client = OpenAI( api_key=os.environ.get("API_KEY") )

# FastAPI 인스턴스 생성
app = FastAPI()

# 챗봇 생성
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

# 요청 형식을 정의하는 Pydantic 모델
class Query(BaseModel):
    question: str

# 질문을 받아 챗봇의 응답을 반환하는 엔드포인트
@app.post("/ask")
async def ask_math_tutor(query: Query):
    try:
        # 새로운 대화 쓰레드 생성
        thread = client.beta.threads.create()
        
        print("thread.id >>>> ",thread.id) # thread_HvBQR1E24zyBXDEnlnoKiB4Q

        # 사용자 메시지를 Thread에 저장
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query.question
        )

        # Run 실행 및 완료 대기
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please address the user as Jane Doe. The user has a premium account."
        )

        # Run이 완료되었는지 확인
        if run.status == 'completed':
            # 대화 메시지 목록 가져오기
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            # 응답 메시지 추출 및 반환
            response_text = ""
            for message in messages.data:
                if message.role == "assistant":  # 챗봇의 응답만 추출
                    for content_block in message.content:
                        response_text += content_block.text.value + "\n"

            return {"response": response_text.strip()}
        else:
            raise HTTPException(status_code=500, detail=f"Run status: {run.status}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 특정 Thread의 전체 메시지 리스트를 반환하는 엔드포인트
@app.get("/threads/{thread_id}")
async def get_thread_messages(thread_id: str):
    try:
        # 대화 메시지 목록 가져오기
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        # 메시지 데이터를 리스트 형식으로 변환
        messages_list = []
        for message in messages.data:
            message_data = {
                "message_id": message.id,
                "role": message.role,
                "content": [block.text.value for block in message.content],
                "created_at": message.created_at,
            }
            messages_list.append(message_data)

        return {"messages": messages_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
