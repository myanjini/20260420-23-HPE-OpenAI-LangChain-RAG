from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

EXAMPLE_SHOTS = [
    {"role": "user", "content": "Q: 사과"}, 
    {"role": "assistant", "content": "A: red"},
    {"role": "user", "content": "Q: 꽃"}, 
    {"role": "assistant", "content": "A: red, white, yello"},
]

# 사용자가 원하는 답변 형식
# Q: 무지개
# A: red, orange, yellow, green, blue, indigo, violet 
response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.",
    input=EXAMPLE_SHOTS + [{"role":"user", "content": "Q: 무지개"}],
)

print(response.output_text)