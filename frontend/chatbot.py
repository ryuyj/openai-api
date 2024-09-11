import requests
import streamlit as st

# 백엔드에 질문을 보내는 함수
def send_question(question, backend_url):
    try:
        # 백엔드에 POST 요청을 보내고 응답을 받음
        response = requests.post(f"{backend_url}/ask", json={"question": question})
        if response.status_code == 200:
            return response.json()  # 백엔드로부터 응답 데이터 반환
        else:
            st.error("백엔드 서버와 통신하는 중 오류가 발생했습니다.")
            return None
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        return None


# 입력 필드를 제출할 때 실행되는 함수
def submit_question(scroll_placeholder, backend_url):
    user_input = st.session_state.input_field  # 세션 상태에서 입력값 가져오기

    if user_input:
        # 사용자 질문을 대화 기록에 추가
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # 백엔드로 질문 전송 후 응답 받기
        response_data = send_question(user_input, backend_url)
        if response_data:
            # 백엔드 응답을 대화 기록에 추가
            st.session_state.conversation.append({"role": "assistant", "content": response_data["response"]})

    scroll_to_latest(scroll_placeholder)


# 대화 기록 출력 함수 (최신 대화까지 스크롤)
def scroll_to_latest(scroll_placeholder):
    with scroll_placeholder.container():
        for chat in st.session_state.conversation:
            if chat["role"] == "user":
                # 사용자 질문은 파란색으로 표시
                st.markdown(f'<p style="color:blue; font-weight:bold;">User: {chat["content"]}</p>',
                            unsafe_allow_html=True)
            else:
                # 챗봇 응답은 녹색으로 표시
                st.markdown(f'<p style="color:green; font-style:italic;">Chatbot: {chat["content"]}</p>',
                            unsafe_allow_html=True)
