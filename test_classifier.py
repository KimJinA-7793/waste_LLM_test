from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# .env 파일에서 API 키 불러오기
# Gemini 클라이언트 생성
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

# 이미지 파일 경로 (여기에 실제 파일명 입력)
image_path = "test_vinyl.jpg"  #같은 워크스페이스 내에 있어야함

# 분리수거 판단 프롬프트
prompt = """
이 쓰레기 사진을 분석해주세요.

**중요 규칙:**
- 그림자, 반사광은 내용물이 아닙니다
- 라벨, 띠지, 스티커는 오염물이 아닙니다
- **캔/병의 인쇄된 그래픽, 로고, 디자인은 정상입니다**
- **금속 표면의 찌그러짐과 그림자는 정상입니다**
- 명확한 음식물/액체 오염만 지적하세요
- 깨끗해 보이면 낮은 확신도로 판단하세요

**판단 기준:**
- 오염 확신도 50% 이상 → 세척필요
- 오염 확신도 15% 이상 50% 미만 → 확인 및 세척권장
- 오염 확신도 15% 미만 → 가능

**분리배출 추가 안내:**
- 페트병/유리병: 라벨과 뚜껑 분리
- 캔: 완전히 비우고 헹굼
- 비닐: 이물질 제거

**질문:**
1. 종류: [플라스틱/유리/종이/비닐/캔 중 하나만]
2. 오염 확신도: [0-100%]
3. 판단: [가능/확인 및 세척권장/세척필요]
4. 추가 처리: [라벨 분리, 뚜껑 분리 등 - 해당사항 있을 때만 명시]

이 형식으로만 간결하게 답변하세요.
"""

# 이미지 파일 업로드 #AI에서는 path = ~ 이라고 알려주는 경우가 많은데 file = ~이 최신 ver임
uploaded_file = client.files.upload(file = image_path)

# LLM에게 이미지와 함께 질문
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[prompt, uploaded_file]
)

print("=== 쓰레기 분류 결과 ===")
print(response.text)

# 업로드한 파일 삭제 (선택사항)
client.files.delete(name=uploaded_file.name)