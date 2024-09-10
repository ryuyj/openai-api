

# 파이썬 학습 도우미 클래스
class PythonLearningAssistant:
    # 클래스 초기화 메서드
    def __init__(self, openai_client, assistant_name="Python Learning Assistant"):  
        self.client = openai_client  # OpenAI 클라이언트 객체 설정
        self.assistant_name = assistant_name  # 어시스턴트 이름 설정
        self.assistant = None  # 어시스턴트 객체 초기화
        self.vector_store = None  # 벡터 저장소 객체 초기화

# 어시스턴트 및 벡터 저장소 설정 메서드
    def setup_assistant(self):  
        self.assistant = self.client.create_assistant(
            name=self.assistant_name,
            instructions="너는 파이썬 학습 도우미야. 첨부된 파일을 사용하여 파이썬에 대한 질문에 답변해줘.",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )
        self.vector_store = self.client.create_vector_store(name="Python Learning")
        print(f"Created vector store: {self.vector_store.id}")

# 학습 자료 업로드 메서드
    def upload_learning_material(self, file_paths):  
        file_batch = self.client.upload_files(
            vector_store_id=self.vector_store.id, file_paths=file_paths
        )
        print(f"File batch status: {file_batch.status}")  # 파일 업로드 상태 출력
        print(f"File counts: {file_batch.file_counts}")  # 업로드된 파일 개수 출력

        self.client.update_assistant(
            assistant_id=self.assistant.id, vector_store_id=self.vector_store.id
        )

# 스레드 생성 메서드
    def create_learning_thread(self, question, file_path):  
        #message_file = self.client.create_message_file(file_path)
        #thread = self.client.create_thread(content=question, file_id=message_file.id)
        thread = self.client.create_thread(content=question) 
        print(f"Thread created with ID: {thread.id}")
        return thread

# 스레드 응답 출력 메서드
    def display_thread_responses(self, thread_id, run_id):  
        messages = self.client.list_thread_messages(thread_id, run_id)
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.retrieve_file(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)  # 메시지 내용 출력
        print("\n".join(citations))  # 파일 출처 출력

