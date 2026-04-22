from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import FileChatMessageHistory

load_dotenv()
model = ChatOpenAI(model="gpt-4.1-nano")

history = FileChatMessageHistory(file_path="./history.json")

while True:
    user_input = input("사용자: ")
    if user_input.lower() == "exit":
        break

    history.add_user_message(user_input)

    ai_message = model.invoke(history.messages)
    history.add_ai_message(ai_message)

    print(f"상담사: {ai_message.content}")
    print()


print("-" * 50)
print(history.messages)
for message in history.messages:
    print(message.content)
