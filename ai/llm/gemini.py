from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.gemini import Gemini
from model.restaurant import GoogleRestaurant, HandwritingText

from dotenv import load_dotenv
from enum import StrEnum
import os


class GeminiModel(StrEnum):
    GEMINI_1_5_FLASH = 'models/gemini-1.5-flash',
    GEMINI_2_0_FLASH = 'models/gemini-2.0-flash-exp',

class GeminiLLM():

    def __init__(self, model: GeminiModel) -> None:
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.llm = GeminiMultiModal(
            model=model,
            api_key=self.api_key,  # uses GOOGLE_API_KEY env var by default
        )

    def chat(self, content):
       return self.llm.complete(content)

    def chat_with_images(self, images, prompt):
        # resp = self.pydantic_gemini(GoogleRestaurant, images, prompt,)
        # print(resp)
        results = []
        for img_doc in images:
            pydantic_response = self.pydantic_gemini(GoogleRestaurant, [img_doc], prompt,)
            if "miami" in img_doc.image_path:
                for r in pydantic_response:
                    print(r)
            results.append(pydantic_response)
    

    def pydantic_gemini(self, output_class, image_documents, prompt_template_str):
        llm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(output_class),
            image_documents=image_documents,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,
            verbose=True,
        )
        response = llm_program()
        return response

    def get_handwriting(self):
        prompt_template_str = """\
            请提取出图片中的文字 \
        """ 
        images = SimpleDirectoryReader("/Users/tju/Workspace/projects/sts/svr/files/handwriting").load_data()
        print(len(images))

        llm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(HandwritingText),
            image_documents=images,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=self.llm,)
        resp = llm_program()
        print(resp)
    
    def get_google_restaurants(self):

        prompt_template_str = """\
            there are several images in this conversation, can you summarize what are in the image\
            and return the answer with json format \
        """
        google_image_documents = SimpleDirectoryReader(
            "/Users/tju/Workspace/projects/sts/svr/files/google_restaurants"
        ).load_data()
        self.chat_with_images(google_image_documents, prompt_template_str)

 