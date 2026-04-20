from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."}, 
        {"role": "user", "content": "홍길동전을 두 문장으로 요약해줘."}
    ],
    stream=True
)

# print(response)
# print(response.choices[0].message.content)

for chunk in response:
    # print(chunk)
    if chunk.choices[0].finish_reason == None:
        print(chunk.choices[0].delta.content, end="|", flush=True)