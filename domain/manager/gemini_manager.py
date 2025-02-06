
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
MINIO_END_POINT=os.getenv("MINIO_END_POINT")
MINIO_URL = f'http://{MINIO_END_POINT}/assignments/'

review_manager = ReviewManager()
llm = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
agent = AssignmentAgent(llm.gemini)


class GeminiManager:

    def review(self, request_id: str,  directory: str,  files: List[str]):
        """ review assignments and save the results to database"""

        """将MINIO上的文件下载到本地"""
        path = f'{LOCAL_IMAGE_ROOT_DIR}/{directory}'
        if not os.path.exists(path=path):
            os.makedirs(path)
        self.download_files(path, files)

        review_info = agent.check_assignments(directory=directory)
        if review_info is None:
            return
        review_ai, details = review_manager.create_ai_review_info(request_id, review_info)
        if review_ai is None or details is None:
            return
        session.add(review_ai)
        for detail in details:
            session.add(detail)
        session.commit()

        try:
            shutil.rmtree(directory)
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



