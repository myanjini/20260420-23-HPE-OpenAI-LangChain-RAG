from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("💬 Chatbot ^___^")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# 대화 내용을 저장할 변수를 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "How can I help you?"},
    ]

with st.sidebar:
    # 업로드 파일을 저장할 변수를 초기화
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = set()

    # 새로운 파일을 추가한 경우 
    uploaded_file = st.file_uploader("요약할 파일을 선택해 주세요.")
    if (uploaded_file is not None and 
        uploaded_file not in st.session_state.uploaded_files):
        
        st.session_state.messages.append({
            "role": "user", 
            "content": f"{uploaded_file.name} 파일 내용을 요약합니다."
        })

        # 업로드한 파일을 서버에 저장 
        with open(uploaded_file.name, "wb") as file:
            bytes_data = uploaded_file.getvalue()
            file.write(bytes_data)

        # 저장된 PDF 파일을 전달해서 요약한 내용을 마크다운 형식으로 반환
        from step4_all_together import summarize_pdf_file_to_markdown
        summary = summarize_pdf_file_to_markdown(uploaded_file.name)

        # LLM 응답을 대화 내용에 추가 
        st.session_state.messages.append(
            {"role": "assistant", "content": summary}
        )

        # 업로드 파일을 저장할 변수에 업로드 파일을 추가
        st.session_state.uploaded_files.add(uploaded_file)


# 대화 내용을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력을 대기
if prompt := st.chat_input():

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