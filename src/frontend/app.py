import streamlit as st
from chatbot import submit_question, scroll_to_latest

# 백엔드 서버 URL (FastAPI 서버 주소)
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI 서버 주소와 포트

# 대화 내용을 저장할 리스트를 세션 상태로 관리
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # 대화 기록 초기화

####################################
# Streamlit 애플리케이션 UI 설정
####################################

st.title("Math Tutor Chatbot")
st.write("수학 문제에 대한 질문을 입력하세요.")

# 대화 기록을 출력하는 부분
st.subheader("대화 기록 (오래된 순)")

# 스크롤 위치를 설정할 빈 placeholder
scroll_placeholder = st.empty()

# 스크롤을 위한 placeholder를 함수에 전달
scroll_to_latest(scroll_placeholder)

# 입력 폼은 항상 하단에 배치
st.write("---")
st.write("질문을 입력하세요:")

# 입력 필드와 'Send' 버튼을 사용한 폼 관리 (하단에 위치)
with st.form("myform", clear_on_submit=True):
    st.text_input(
        "질문 입력:",  # 명확한 label 제공
        key="input_field",  # 세션 상태 키를 새로운 키로 설정
        max_chars=200,
        label_visibility="collapsed",  # Label 숨기기
    )

    submit = st.form_submit_button(label="Send")

# 'Send' 버튼을 누르면 질문 제출
if submit:
    submit_question(scroll_placeholder, BACKEND_URL)
