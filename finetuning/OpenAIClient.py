from openai import OpenAI



# OpenAI 클라이언트 초기화
class OpenAIClient:
    def __init__(self):  # 클래스 초기화 메서드
        self.client = OpenAI()  # OpenAI API 클라이언트를 초기화

    # 어시스턴트 생성 메서드
    def create_assistant(self, name, instructions, model, tools):  
        return self.client.beta.assistants.create(
            name=name,  # 어시스턴트 이름
            instructions=instructions,  # 어시스턴트에게 주어진 지침
            model=model,  # 사용할 모델 지정
            tools=tools,  # 사용할 도구 지정
        )

    # 벡터 저장소 생성 메서드
    def create_vector_store(self, name):  
        return self.client.beta.vector_stores.create(name=name)

    # 파일 업로드 메서드
    def upload_files(self, vector_store_id, file_paths):  
        file_streams = [open(path, "rb") for path in file_paths]  # 파일 경로를 바이너리로 열기
        return self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id, files=file_streams  # 파일들을 벡터 저장소에 업로드
        )

    # 어시스턴트 업데이트 메서드
    def update_assistant(self, assistant_id, vector_store_id):  
        return self.client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store_id]  # 벡터 저장소 ID 업데이트
                }
            },
        )

    # def create_message_file(self, file_path):  # 메시지 파일 생성 메서드
    #     return self.client.files.create(
    #         file=open(file_path, "rb"),  # 파일을 바이너리로 열기
    #         purpose="assistants"  # 파일 목적 설정
    #     )

    # 스레드 생성 메서드
    def create_thread(self, content, file_id):  # 스레드 생성 메서드
        return self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",  # 메시지 작성자 역할 설정
                    "content": content  # 사용자 질문 내용
                    # "attachments": [
                    #     { "file_id": file_id, "tools": [{"type": "file_search"}] }  # 파일 첨부 및 도구 설정
                    # ],
                }
            ]
        )
    
# 파일 검색 메서드
    def retrieve_file(self, file_id):  
        return self.client.files.retrieve(file_id)
    
# 스레드 메시지 목록 가져오기 메서드
    def list_thread_messages(self, thread_id, run_id):  
        return list(self.client.beta.threads.messages.list(thread_id=thread_id, run_id=run_id))
