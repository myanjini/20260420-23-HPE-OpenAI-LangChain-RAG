from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# 대화 내용을 기록할 리스트를 정의
conversations = []

while True:
    user_input = input("사용자: ")
    if user_input == "exit":
        break

    # 사용자 입력(질문)을 대화 내용에 추가 
    conversations.append({"role": "user", "content": user_input})
        
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="당신은 사용자를 도와주는 상담사입니다.",
        input=conversations,
    )

    # 모델 응답을 대화 내용에 추가
    conversations.append({"role": "assistant", "content": response.output_text})

    print("상담사: ", response.output_text)
    print()


# 대화 종료 후 대화 내용을 출력
print("\n대화 내용\n" + "-" * 50)
for message in conversations:
    print(f"{message['role']:>9}: {message['content']}")
