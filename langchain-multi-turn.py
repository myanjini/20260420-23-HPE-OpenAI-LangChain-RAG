from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 모델 초기화
load_dotenv()
model = ChatOpenAI(model="gpt-4.1-nano")

# 대화 내용을 기록할 리스트
messages = [SystemMessage(content="너는 사용자를 도와주는 친절한 상담사야.")]

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    ai_response = model.invoke(messages)
    messages.append(ai_response)

    print(f"상담사: {ai_response.content}")
    print()

    print(">" * 50)
    for i, msg in enumerate(messages):
        print(f"{i:<3} {msg.__class__.__name__:<15} {msg.content[:50]}")
    print("<" * 50)
    print()
