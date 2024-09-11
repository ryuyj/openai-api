from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI 클라이언트 인스턴스 생성
client = OpenAI(
    api_key=os.environ.get("API_KEY")  # "API_KEY"라는 이름으로 저장된 환경 변수에서 API 키를 가져옵니다.
)

response = client.images.generate(
  model="dall-e-3",  # 모델 지정
  prompt="a white siamese cat",  # 텍스트 프롬프트 입력
  size="1024x1024",  # 이미지 크기 지정
  quality="standard",  # 이미지 품질 설정
  n=1,  # 생성할 이미지 수
)

print(response.data)  # 생성된 이미지 URL 출력
image_url = response.data[0].url  # 생성된 이미지 URL 가져오기
print('URL >>>>', image_url)  # 생성된 이미지 URL 출력