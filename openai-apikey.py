from dotenv import load_dotenv
import os

# .env 파일 내용을 환경변수로 등록
load_dotenv()				

# OpenAI API Key가 환경변수에 등록된 것을 확인
print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:-50]}{"*"*50}")
