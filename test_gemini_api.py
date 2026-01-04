from google import genai
from dotenv import load_dotenv
import os

# .env 파일에서 API 키 불러오기
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Gemini 클라이언트 생성
client = genai.Client(api_key=api_key)

# 테스트 메시지
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='안녕! 잘 작동하는지 테스트 중이야.'
)

print(response.text)