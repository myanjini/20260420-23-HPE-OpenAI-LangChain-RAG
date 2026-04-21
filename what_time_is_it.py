from functions_v1 import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv

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


# 대화 내용을 기록할 리스트
input_list = []

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    input_list.append({"role": "user", "content": user_input})

    response = get_ai_response(input_list, tools=tools)
    input_list += response.output

    # 함수 호출이 있으면 함수 실행 후 결과를 질의에 추가 
    is_function_call = False
    for item in response.output:
        if item.type == "function_call":
            is_function_call = True
            if item.name == "get_current_time":
                function_result = get_current_time()
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id, 
                    "output": function_result
                })

    # 함수 호출이 있는 경우 함수 실행 결과를 모델에게 전달 
    if is_function_call:
        response = get_ai_response(input_list)
        input_list += response.output

    # 답변을 출력
    # print(response)
    print(response.output_text)
    print()
