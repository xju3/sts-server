import base64
import requests


def encode_image(image_path):
    """Convert image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class OllamaImageChat:

    def __init__(self, image_file_name) -> None:
        self.image_file_name = image_file_name
   
    def run(self):
        image_base64 = encode_image(self.image_file_name)

        # Send the image to Ollama for processing
        url = "http://localhost:11434/api/generate"  # Ollama API endpoint
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llava",  # Use a multimodal model like Llava
            "prompt": "Describe this image in detail.",
            "images": [image_base64]
        }

        response = requests.post(url, json=data, headers=headers)
        image_description = response.json().get("response", "")
        print("Ollama Response:", image_description)
        return image_description
