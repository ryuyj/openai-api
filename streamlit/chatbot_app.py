import streamlit as st

# Streamlit 애플리케이션 UI 설정
st.title("Math Tutor Chatbot")
st.write("수학 문제에 대한 질문을 입력하세요.")
    
# 대화 기록을 출력하는 부분
st.subheader("대화 기록 (오래된 순)")

# 입력 폼은 항상 하단에 배치
st.write("---")
st.write("질문을 입력하세요:")

# 입력 필드와 'Send' 버튼을 사용한 폼 관리 (하단에 위치)
with st.form("myform", clear_on_submit=True):
    st.text_input(
        "질문 입력:",  # 명확한 label 제공
        max_chars=200,
        label_visibility="collapsed",  # Label 숨기기
    )
    
    submit = st.form_submit_button(label="Send")

