from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 모델 초기화
load_dotenv()
# model = ChatOpenAI(model="gpt-4.1-nano")
model = OllamaLLM(model="llama3.1:8b", temperature=0.7)

# 대화 내용을 기록할 리스트
messages = [SystemMessage(content="너는 사용자를 도와주는 친절한 상담사야.")]

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    ai_response = model.invoke(messages)
    messages.append(AIMessage(content=ai_response))

    # print(ai_response)

    print(f"상담사: {ai_response}")
    print()

    print(">" * 50)
    for i, msg in enumerate(messages):
        print(f"{i:<3} {msg.__class__.__name__:<15} {msg.content[:50]}")
    print("<" * 50)
    print()
