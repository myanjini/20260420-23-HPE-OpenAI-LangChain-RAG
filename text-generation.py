from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "user",
            "content": "OpenAI Chat Completions API에 대해 한 문장으로 설명해줘.",
        },
    ],
)

print(completion)
print(completion.choices[0].message.content)
