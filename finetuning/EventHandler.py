from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

# 이벤트 핸들러 클래스
class EventHandler(AssistantEventHandler):  

# 텍스트 생성 이벤트 처리    
    @override
    def on_text_created(self, text) -> None:  
        print(f"\nassistant > {text}", end="", flush=True)

# 도구 호출 이벤트 처리
    @override
    def on_tool_call_created(self, tool_call):  
        print(f"\nassistant > {tool_call.type}\n", flush=True)

# 메시지 완료 이벤트 처리
    @override
    def on_message_done(self, message) -> None:  
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))
