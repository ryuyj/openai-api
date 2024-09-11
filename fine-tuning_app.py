from openai import OpenAI
import os

client = OpenAI( api_key=os.environ.get("API_KEY") )

# 미세 조정을 위한 학습 파일 업로드
train_file = client.files.create(
  file=open("./finetuning/data/data10.jsonl", "rb"),
  purpose="fine-tune"
)

# 미세 조정 작업 생성
client.fine_tuning.jobs.create(
  training_file=train_file.id, # 학습 파일을 OpenAI API에 업로드할 때 반환된 파일 ID
  model="gpt-3.5-turbo" # 미세 조정하려는 모델의 이름
)


# 10가지 미세 조정 작업 목록
jobs_list = client.fine_tuning.jobs.list(limit=10)
print(jobs_list)
