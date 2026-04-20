from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

EXAMPLE_SHOTS = [
    {"role": "user", "content": "참새"},
    {"role": "assistant", "content": "짹짹!!!"},
    {"role": "user", "content": "병아리"},
    {"role": "assistant", "content": "삐악삐악!!!"},
    {"role": "user", "content": "뱀"},
    {"role": "assistant", "content": "(조용)"},
]


def run_prompt_test(animal: str, shot_count: int):
    input = EXAMPLE_SHOTS[: shot_count * 2] + [{"role": "user", "content": animal}]
    try:
        response = client.responses.create(
            model="gpt-3.5-turbo",
            max_output_tokens=100,
            instructions="당신은 어린이집을 다니는 7살 아이입니다. 모든 질문에 대해 한 문장으로 답변해 주세요.",
            input=input,
        )
        output_text = response.output_text
    except Exception as e:
        output_text = f"API 호출 오류: {e}"
    finally:
        print(f"{animal} >>> {output_text}")


if __name__ == "__main__":
    animals = ["강아지", "호랑이", "도마뱀"]

    print(f"\nZero-shot\n{'-'*50}")
    for animal in animals:
        run_prompt_test(animal, 0)

    print(f"\nOne-shot\n{'-'*50}")
    for animal in animals:
        run_prompt_test(animal, 1)

    print(f"\nTwo-shot\n{'-'*50}")
    for animal in animals:
        run_prompt_test(animal, 2)

    print(f"\nFew-shot\n{'-'*50}")
    for animal in animals:
        run_prompt_test(animal, 3)
