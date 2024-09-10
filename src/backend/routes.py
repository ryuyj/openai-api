from fastapi import APIRouter, HTTPException
from models import Query
from services import (
    add_message_to_thread,
    execute_run,
    list_thread_messages,
    extract_assistant_responses
)
from config import assistant_id, thread_id

router = APIRouter()

# 질문을 받아 챗봇의 응답을 반환하는 엔드포인트
@router.post("/ask")
async def ask_math_tutor(query: Query):
    try:
        # 기존의 스레드에 메시지 추가
        add_message_to_thread(thread_id=thread_id, role="user", content=query.question)
        
        # Run 실행 및 완료 대기
        run = execute_run(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions="Please address the user as Jane Doe. The user has a premium account."
        )

        if run.status == 'completed':
            messages = list_thread_messages(thread_id=thread_id)
            response_text = extract_assistant_responses(messages)
            return {"response": response_text, "thread_id": thread_id}
        else:
            raise HTTPException(status_code=500, detail=f"Run status: {run.status}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 특정 Thread의 전체 메시지 리스트를 반환하는 엔드포인트
@router.get("/threads/{thread_id}")
async def get_thread_messages(thread_id: str):
    try:
        messages_list = list_thread_messages(thread_id)
        return {"messages": messages_list, "thread_id": thread_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
