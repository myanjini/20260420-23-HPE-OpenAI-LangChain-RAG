from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot ^___^")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# 대화 내용을 저장할 변수를 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "How can I help you?"},
    ]

# 대화 내용을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력을 대기
if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = OpenAI(api_key=openai_api_key)
    client = OpenAI()

    # 사용자 입력을 대화 내용에 추가하고 화면에 출력
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)

    # LLM 호출
    with st.spinner("Wait for it ..."):
        response = client.responses.create(
            model="gpt-3.5-turbo", 
            input=st.session_state.messages
        )

        # LLM 응답에서 텍스트를 추출
        msg = response.output_text

        # LLM 응답을 대화 내용에 추가하고 화면에 출력
        st.session_state.messages.append(
            {"role": "assistant", "content": msg}
        )
        st.chat_message("assistant").write(msg)