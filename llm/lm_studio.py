
from llama_index.llms.lmstudio import LMStudio
from dotenv import load_dotenv
from enum import StrEnum

class LmStudioModel(StrEnum):
    QWEN_2_5_CODER_14_B= 'qwen2.5-coder-14b-instruct-mlx',

class LmStudioQwenCode14b:
    def __init__(self, model:LmStudioModel) -> None:
        load_dotenv()
        self.llm = LMStudio(base_url="http://localhost:3011/v1", 
                            model_name=model)
    def chat(self, content: str):
       return self.llm.complete(content)