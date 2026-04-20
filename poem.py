from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {
            "role": "user",
            "content": "'아울렛'을 주제로 짧은 동시를 하나 작성해줘.",
        },
    ],
    temperature=1.2
)

print(completion.choices[0].message.content)
