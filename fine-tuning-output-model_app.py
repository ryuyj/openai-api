from openai import OpenAI
import os

client = OpenAI( api_key=os.environ.get("API_KEY") )


completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::A1oYG3JX",
  messages=[
    {"role": "system", "content": "질문에 답변해줘"},
    {"role": "user", "content": "미국의 수도가 어디야?"},
  ]
)
print(completion.choices[0].message)


