import streamlit as st
from retriever import retrieve_and_answer

st.title("RAG 기반 챗봇")
st.markdown("---")

# 대화 내용을 기록할 변수를 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 내용을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력을 처리
if user_input := st.chat_input("질문을 입력하세요..."):
    # 사용자 입력을 화면에 출력하고 대화 내용에 기록
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # RAG 모델을 통해 답변 생성
    answer = retrieve_and_answer(user_input)

    # 모델의 답변을 화면에 출력하고 대화 내용에 기록
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})