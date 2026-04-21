from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()


def summarize_text(text: str) -> str:
    instructions = """
        당신은 요약 전문가 입니다. 

        제공하는 내용에서 글쓴이의 문제 인식과 주장, 주요 내용, 글쓴이 소개를 제시한 형식에 맞춰서 요약합니다.
        
        # 제목 

        ## 글쓴이의 문제 인식과 주장 (10 문장 이내)

        ## 주요 내용
        
        ## 글쓴이 소개
        - 글쓴이 1
        - 글쓴이 2
        - 글쓴이 3
    """

    response = client.responses.create(
        model="gpt-4.1-nano",
        temperature=0.3,
        instructions=instructions,
        input=f"다음 내용을 요약해 주세요.:\n\n{text}",
    )
    return response.output_text


def text_summary_to_md_file(preprocessed_text_file_path: str) -> str:
    with open(preprocessed_text_file_path, "r", encoding="utf-8") as file:
        text = file.read()

    md_file_path = preprocessed_text_file_path.replace(".txt", "-summarized.md")

    with open(md_file_path, "w", encoding="utf-8") as file:
        file.write(summarize_text(text))

    return os.path.abspath(md_file_path)


if __name__ == "__main__":
    preprocessed_file_path = "./data/crop-model-preprocessed.txt"

    markdown_file_path = text_summary_to_md_file(preprocessed_file_path)
    print(markdown_file_path)
