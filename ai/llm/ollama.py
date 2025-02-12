

from llama_index.llms.ollama import Ollama
from enum import StrEnum
from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from llama_index.core.output_parsers import PydanticOutputParser
from ai.agent.agent import GoogleRestaurant



class OllamaTextModels(StrEnum):
    DEEP_SEEK_R_1_14 = 'deepseek-r1:14b',
    CODE_LLAMA_LATEST = 'codellama:latest',

class OllamaMMModels(StrEnum):
    LLAVA_LATEST = 'llava:latest',

class OllamaTextLLM: 
    def __init__(self, model : OllamaTextModels) -> None:
        self.llm = Ollama(base_url='https://localhost:11434', api_key='', model=model)

    def chat(self, content: str):
       return self.llm.complete(content)

class OllamaMultiModalLLM:

    def __init__(self, model: OllamaMMModels) -> None:
        self.llm = OllamaMultiModal(model=model, base_url='http://localhost:11434')

    def chat_with_images(self, images, prompt):
        pass

    def get_restaurant_info(self):
        image_documents = SimpleDirectoryReader("/Users/tju/Workspace/projects/sts/svr/files/images").load_data()
        prompt_template_str = """\
        {query_str}

        Return the answer as a Pydantic object. The Pydantic schema is given below:

        """
        mm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(GoogleRestaurant),
            image_documents=image_documents,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
            verbose=True,
        )

        response = mm_program(query_str="Can you summarize what is in the image?")
        for res in response:
            print(res)


    