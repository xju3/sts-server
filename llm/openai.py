from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

class OpenAI_O3_Mini(): 

    def __init__(self) -> None:
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(api_key=openai_api_key, model='o3-mini')

    def chat(self, content: str):
       return self.llm.complete(content)
    