from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

class DallEClient:
  def __init__(self):
    # OpenAI API 클라이언트를 초기화합니다.
    self.client = OpenAI(
      api_key=os.environ.get("API_KEY")  # 환경 변수에서 API 키를 가져옵니다.
    )

  def generate_image(self, prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
    response = self.client.images.generate(
      model=model,  # 모델 지정
      prompt=prompt,  # 텍스트 프롬프트 입력
      size=size,  # 이미지 크기 지정
      quality=quality,  # 이미지 품질 설정
      n=n,  # 생성할 이미지 수
    )
    return response.data

# 스크립트가 직접 실행될 때만 아래의 코드가 실행됩니다.
if __name__ == "__main__":
  
    # DallEClient 클래스의 인스턴스를 생성합니다. 이 클래스는 Dall-E 모델과의 상호작용을 담당합니다.
    dall_e_client = DallEClient()
    
    # 사용자로부터 이미지 설명(prompt)을 입력받습니다.
    prompt = input("Please enter a Image Decription: ")
    
    
    # 사용자가 입력한 프롬프트를 기반으로 이미지를 생성합니다.
    # 생성된 이미지는 images 변수에 리스트 형태로 저장됩니다.
    images = dall_e_client.generate_image(prompt)
    
    # images 리스트의 각 이미지와 그 인덱스를 반복합니다.
    for idx, image in enumerate(images):
        # 각 이미지 객체의 url 속성을 가져와 image_url 변수에 저장합니다.
        image_url = image.url
        # 생성된 각 이미지의 URL을 출력합니다. 인덱스는 1부터 시작하도록 idx + 1로 표시합니다.
        print(f"Image {idx + 1} URL >>> {image_url}")
        
