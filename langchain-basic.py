from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4.1-nano")

message = HumanMessage(content="안녕? 나는 홍길동이야.")
response = model.invoke([message])
print(f"User: {message.content}")
print(f"AI: {response.content}")

print()

message = HumanMessage(content="내 이름이 뭐지?")
response = model.stream([message])
print(f"User: {message.content}")
# print(f"AI: {response.content}")
print("AI: ", end="")
for chunk in response:
    # print(type(chunk), chunk)
    print(chunk.content, end="|", flush=True)
