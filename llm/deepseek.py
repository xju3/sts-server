
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

class DeepseekChatBot: 

    def __init__(self) -> None:
        load_dotenv()
        ds_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.llm = OpenAI(base_url='https://api.deepseek.com', api_key=ds_api_key)

    def chat(self, content: str):
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": content} ]
        resp = self.llm.chat.completions.create(model="deepseek-chat",messages=messages,stream=False)
        return resp.choices[0].message.content