import streamlit as st

# 세션 상태에서 초기값 설정
if 'text_input_value' not in st.session_state:
    st.session_state['text_input_value'] = ""

# 입력 필드 생성
text_value = st.text_input("Enter text", value=st.session_state['text_input_value'])

# 입력값을 초기화하는 함수 정의
def reset_input():
    st.session_state['text_input_value'] = ""

# 버튼을 클릭하면 입력값 초기화
if st.button("Reset"):
    reset_input()
    st.experimental_rerun() 

st.write(f"Current input: {text_value}")
