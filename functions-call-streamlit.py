from functions_v3 import get_current_time, get_yf_stock_info, tools
from openai import OpenAI
from dotenv import load_dotenv
import json
import streamlit as st

load_dotenv()
client = OpenAI()

# 모델에 질의하고 질의 결과를 반환하는 함수
def get_ai_response(input_list, tools=None):
    print("messages >>> ...")
    for i, msg in enumerate(input_list):
        print(f"{i}\t{msg}")
    print()

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 친절한 비서입니다.",
        input=input_list,
        tools=tools,
        tool_choice="auto",
    )

    print("... >>> response.output")
    print(response.output)
    print()

    return response


# (LLM 질의에 사용할) 대화 내용을 기록할 리스트를 초기화
if "input_list" not in st.session_state:
    st.session_state.input_list = []

# 스트림릿 앱 설정
st.title("함수 호출을 지원하는 챗봇")

# 화면 출력에 사용할 대화 내용을 기록할 리스트를 초기화
# - 도구 호출과 관련된 내용을 포함하지 않음
# - 사용자 질의와 LLM 최종 응답만 포함
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 내용을 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# while True:
#     user_input = input("사용자: ")
#     if user_input.lower() == "exit":
#         break
# 사용자 입력을 처리
if user_input := st.chat_input():
    # 사용자 입력을 화면에 출력하고 대화 내용에 추가 
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({
        "role": "user", "content": user_input
    })

    st.session_state.input_list.append({
        "role": "user", "content": user_input
    })

    response = get_ai_response(st.session_state.input_list, tools=tools)
    st.session_state.input_list += response.output

    # 함수 호출이 있으면 함수 실행 후 결과를 질의에 추가 
    is_function_call = False
    for item in response.output:
        if item.type == "function_call":
            is_function_call = True

            arguments = json.loads(item.arguments)

            if item.name == "get_current_time":
                function_result = get_current_time(timezone=arguments.get("timezone"))
            elif item.name == "get_yf_stock_info":
                function_result = get_yf_stock_info(ticker=arguments.get("ticker"))
                
            st.session_state.input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id, 
                "output": function_result
            })

    # 함수 호출이 있는 경우 함수 실행 결과를 모델에게 전달 
    if is_function_call:
        response = get_ai_response(st.session_state.input_list)
        st.session_state.input_list += response.output

    # # 답변을 출력
    # # print(response)
    # print(response.output_text)
    # print()
    # LLM의 최종 답변을 화면에 출력하고 대화 내용에 기록
    st.chat_message("assistant").write(response.output_text)
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response.output_text
    })