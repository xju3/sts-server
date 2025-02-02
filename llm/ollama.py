

from llama_index.llms.ollama import Ollama
from dotenv import load_dotenv
import os


from enum import StrEnum
import os


class OllamaModel(StrEnum):
    DEEP_SEEK_R_1_14 = 'deepseek-r1:14b',
    CODE_LLAMA_LATEST = 'codellama:latest',


class OllamaLLM: 

    def __init__(self, model : OllamaModel) -> None:
        load_dotenv()
        self.llm = Ollama(base_url='https://localhost:11434', api_key='', model=model)

    def chat(self, content: str):
       return self.llm.complete(content)
    