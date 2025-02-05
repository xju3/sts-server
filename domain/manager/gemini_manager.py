
from typing import List
from domain.manager.review_manager import ReviewManager
from domain.model.review import ReviewAI, ReviewDetail
from domain.engine import session
from ai.llm.gemini import GeminiLLM, GeminiModel
from ai.agent.assignment import AssignmentAgent
from urllib.request import urlopen
from dotenv import load_dotenv
import os
import shutil


load_dotenv()
LOCAL_IMAGE_ROOT_DIR = os.getenv("IMAGE_TMP_DIR")
MINIO_HOST=os.getenv("MINIO_HOST")
MINIO_URL = f'http://{MINIO_HOST}/assignments/'
review_manager = ReviewManager()
gemini = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
agent = AssignmentAgent(gemini)


class GeminiManager:

    def review(self, minio_directory: str,  files: List[str]):
        """ review assignments and save the results to database"""

        """将MINIO上的文件下载到本地"""
        path = f'{LOCAL_IMAGE_ROOT_DIR}/{minio_directory}'
        if not os.path.exists(path=path):
            os.makedirs(path)
        self.download_files(path, files)

        review_info = agent.check_assignments(directory=path)
        if review_info is None:
            return
        review_ai, details = review_manager.create_ai_review_info(minio_directory, review_info)
        if review_ai is None or details is None:
            return
        session.add_all(review_ai, details)
        session.commit()

        try:
            shutil.rmtree(minio_directory)
        except OSError as e:
            print(f"Error deleting directory {path}: {e}")


    def download_files(self, path,  files: List[str]):
        for file in files:
            url = f'{MINIO_URL}/{file}'
            file_name = file.split('/')[-1]
            local_file_name = f'{path}/{file_name}'
            try:
                with urlopen(url) as response, open(local_file_name, 'wb') as out_file:
                    data = response.read()
                    out_file.write(data)
            except Exception as e:
                print(f'Error downloading {url}: {e}')



