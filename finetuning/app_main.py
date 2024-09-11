from EventHandler import EventHandler
from OpenAIClient import OpenAIClient
from PythonLearningAssistant import PythonLearningAssistant as PLA


def main():
    # OpenAI 클라이언트 및 학습 도우미 인스턴스 생성
    openai_client = OpenAIClient()
    assistant = PLA(openai_client)

    # 1. 어시스턴트 및 벡터 저장소 설정
    assistant.setup_assistant()

    # 2. 학습 자료 업로드
    assistant.upload_learning_material(file_paths=["path/to/파이썬학습파일.doc"])

    # 3. 사용자 질문을 포함한 스레드 생성
    question = "파이썬에서 리스트와 튜플의 차이점은 무엇인가요?"
    thread = assistant.create_learning_thread(question, "path/to/파이썬학습파일.doc")

    # 4. 스트리밍 사용하여 실행
    with openai_client.client.beta.threads.runs.stream(
        thread_id = thread.id,
        assistant_id = assistant.assistant.id,
        instructions = "사용자가 Jane Doe라고 부르도록 하세요. 사용자는 프리미엄 계정입니다.",
        event_handler = EventHandler(),
    ) as stream:
        stream.until_done()  # 스트리밍 종료될 때까지 대기

    # 5. 스레드의 응답 출력
    run = stream.run
    assistant.display_thread_responses(thread.id, run.id)


if __name__ == "__main__":
    main()