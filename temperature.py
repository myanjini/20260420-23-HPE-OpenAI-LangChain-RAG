from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def generate_response(temperature):
    completion = client.chat.completions.create(
        model="gpt-4.1-nano",	# gpt-5-nano 모델의 경우, temperature 값을 수정할 수 없음 (기본값 1을 가짐)
        messages=[
            {
                "role": "user",
                "content": "'국민한대'라는 나라의 수도(capital)와 국기(national는 무엇입니까?",
            },
        ],
        max_completion_tokens=100,
        temperature=temperature,
    )

    print(f"temperature={temperature}", end=f"\n{'-'*50}\n")
    print(completion.choices[0].message.content, end="\n\n")


generate_response(0)
generate_response(1)
generate_response(2)