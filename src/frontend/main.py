import streamlit as st
from chatbot_module import init_conversation, add_to_conversation, send_question, display_conversation, input_form

# 백엔드 서버 URL
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI 서버 주소와 포트

# 메인 애플리케이션 시작
st.title("Math Tutor Chatbot")
st.write("수학 문제에 대한 질문을 입력하세요.")

# 대화 상태 초기화
init_conversation()

# 스크롤 위치를 설정할 빈 placeholder
scroll_placeholder = st.empty()

# 질문 제출 처리
def submit_question():
    user_input = st.session_state.input_field

    if user_input:
        add_to_conversation("user", user_input)

        # 백엔드로 질문 전송 후 응답 받기
        response_data = send_question(user_input, BACKEND_URL)
        if response_data:
            add_to_conversation("assistant", response_data["response"])

    display_conversation(scroll_placeholder)

# 입력 필드와 'Send' 버튼 처리
if input_form():
    submit_question()
