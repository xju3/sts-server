from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from PIL import Image
import matplotlib.pyplot as plt
from pydantic import BaseModel

class RestaurantAgent:

    def __init__(self) -> None:
        pass

    def run(llm):
        image_documents = SimpleDirectoryReader("../files/images").load_data()
        prompt_template_str = """\
        {query_str}
        Return the answer as a Pydantic object. The Pydantic schema is given below:
        """
        mm_program = MultiModalLLMCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(Restaurant),
            image_documents=image_documents,
            prompt_template_str=prompt_template_str,
            multi_modal_llm=llm,
            verbose=True,
        )
        response = mm_program(query_str="Can you summarize what is in the image?")
        for res in response:
            print(res)



class Restaurant(BaseModel):
    """Data model for an restaurant."""

    restaurant: str
    food: str
    discount: str
    price: str
    rating: str
    review: str