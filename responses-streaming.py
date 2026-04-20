from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    instructions="You are a helpful assistant.",
    input="홍길동전을 한 문장으로 요약해줘.",
    stream=True,
)

print(response)
# print(response.output_text)		# response.output[1].content[0].text

for event in response:
    # print(event)
    if event.type == "response.output_text.delta":
        print(event.delta, end="|", flush=True)