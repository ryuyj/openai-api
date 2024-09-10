from openai import OpenAI
from dotenv import load_dotenv  # 환경 변수를 로드하는 dotenv 라이브러리의 load_dotenv 함수를 임포트합니다.
import os                      # 환경 변수에 접근하기 위해 os 모듈을 임포트합니다.

# .env 파일에서 환경 변수를 로드합니다. 이 파일에 API 키와 같은 중요한 설정 정보를 저장할 수 있습니다.
load_dotenv()

# OpenAI 클라이언트 설정
client = OpenAI( api_key=os.environ.get("API_KEY") )

# 어시스턴트 생성
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="너는 개인 수학 튜터야. 수학 문제에 답하는 코드를 작성하고 실행해줘. 답변은 한글로만 해줘",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

# 어시스턴트 ID 저장
assistant_id = assistant.id

# 단일 스레드 생성 및 저장
thread = client.beta.threads.create()
thread_id = thread.id  # 이 ID를 계속 사용