from config import client
from typing import List

# 사용자 메시지를 Thread에 저장
def add_message_to_thread(thread_id: str, role: str, content: str):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )

# Run 실행 및 완료 대기
def execute_run(thread_id: str, assistant_id: str, instructions: str):
    return client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )

# 특정 스레드의 모든 메시지 가져오기
def list_thread_messages(thread_id: str) -> List[dict]:
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    messages_list = []
    for message in messages.data:
        message_data = {
            "message_id": message.id,
            "role": message.role,
            "content": [block.text.value for block in message.content],
            "created_at": message.created_at,
        }
        messages_list.append(message_data)
    return messages_list

# 챗봇의 응답 메시지 추출
def extract_assistant_responses(messages: List[dict]) -> str:
    # 메시지를 역순으로 탐색하여 최근 응답을 추출
    # messages 리스트는 오래된 순으로 정렬되어 있으므로 역순으로 탐색
    messages = list(reversed(messages))
    
    for message in reversed(messages):
        if message['role'] == "assistant":
            return "\n".join(message['content']).strip()
    return ""  # 응답이 없을 경우 빈 문자열 반환
# def extract_assistant_responses(messages: List[dict]) -> str:
#     response_text = ""
#     for message in messages:
#         if message['role'] == "assistant":
#             response_text += "\n".join(message['content']) + "\n"
#     return response_text.strip()