import requests
import streamlit as st

# 대화 상태 관리
def init_conversation():
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

def add_to_conversation(role, content):
    st.session_state.conversation.append({"role": role, "content": content})

# 백엔드와 통신
def send_question(question, backend_url):
    try:
        response = requests.post(f"{backend_url}/ask", json={"question": question})
        if response.status_code == 200:
            return response.json()
        else:
            st.error("백엔드 서버와 통신하는 중 오류가 발생했습니다.")
            return None
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
        return None

# 대화 출력
def display_conversation(scroll_placeholder):
    with scroll_placeholder.container():
        for chat in st.session_state.conversation:
            if chat["role"] == "user":
                st.markdown(f'<p style="color:blue; font-weight:bold;">User: {chat["content"]}</p>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="color:green; font-style:italic;">Chatbot: {chat["content"]}</p>',
                            unsafe_allow_html=True)

# 입력 필드와 UI
def input_form():
    st.write("---")
    st.write("질문을 입력하세요:")

    with st.form("myform", clear_on_submit=True):
        st.text_input(
            "질문 입력:",
            key="input_field",
            max_chars=200,
            label_visibility="collapsed",
        )

        return st.form_submit_button(label="Send")
