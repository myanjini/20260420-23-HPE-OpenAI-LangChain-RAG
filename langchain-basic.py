from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

# 모델 초기화
# https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html
model = ChatOpenAI(model="gpt-4.1-nano")

# 사용자 메시지를 작성해서 모델에 전달하면 AI 메시지를 응답
message = HumanMessage(content="안녕? 나는 홍길동이야.")
print(type(message))
print(message)
print()

response = model.invoke([message])

print(type(response))
print(response)
print()

print(f"User: {message.content}")
print(f"AI: {response.content}")
print()

print("*" * 50)

message = HumanMessage(content="내 이름이 뭐지?")
response = model.invoke([message])
print(f"User: {message.content}")
print(f"AI: {response.content}")

