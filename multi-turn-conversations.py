from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

conversations = client.conversations.create()

while True:
    user_input = input("사용자: ")
    if user_input == "exit":
        break

    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        input=user_input,
        conversation=conversations.id,
    )

    print("상담사: ", response.output_text)
    print()