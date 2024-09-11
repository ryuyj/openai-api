# openai 및 dotenv 라이브러리를 임포트합니다. 
from openai import OpenAI     # OpenAI 클래스를 사용하기 위해 openai 라이브러리를 임포트합니다.
from dotenv import load_dotenv  # 환경 변수를 로드하는 dotenv 라이브러리의 load_dotenv 함수를 임포트합니다.
import os                      # 환경 변수에 접근하기 위해 os 모듈을 임포트합니다.

# .env 파일에서 환경 변수를 로드합니다. 이 파일에 API 키와 같은 중요한 설정 정보를 저장할 수 있습니다.
load_dotenv()

# OpenAI 클라이언트를 생성하고 환경 변수에서 API 키를 가져와 설정합니다.
client = OpenAI(
    api_key=os.environ.get("API_KEY")  # "API_KEY"라는 이름으로 저장된 환경 변수에서 API 키를 가져옵니다.
)

# 모듈화 
def chat_completions_create(model, messages):
    # OpenAI API를 사용하여 챗봇 응답을 생성합니다.
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # 생성된 챗봇 응답을 반환합니다.
    return completion
