
from typing import List
from domain.manager.review_manager import ReviewManager
from domain.engine import engine
from sqlalchemy.orm import sessionmaker
from ai.llm.gemini import GeminiLLM, GeminiModel
from ai.agent.assignment import AssignmentAgent
from urllib.request import urlopen
from dotenv import load_dotenv
import os, logging, sys
import shutil
from datetime import datetime


load_dotenv()
LOCAL_IMAGE_ROOT_DIR = os.getenv("IMAGE_TMP_DIR")
MINIO_END_POINT=os.getenv("MINIO_END_POINT")
MINIO_URL = f'http://{MINIO_END_POINT}/assignments/'

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, filename='gemini_manager.log')
logger = logging.getLogger()


review_manager = ReviewManager()
llm = GeminiLLM(GeminiModel.GEMINI_2_0_FLASH)
agent = AssignmentAgent(llm.gemini)


class GeminiManager:

    def review(self, request_id: str,  minio_directory: str,  files: List[str]):
        """ review assignments and save the results to database"""

        local_path = f'{LOCAL_IMAGE_ROOT_DIR}/{minio_directory}'
        """将MINIO上的文件下载到本地"""
        if not os.path.exists(path=local_path):
            os.makedirs(local_path)
        self.download_files(local_path, files)
        start_time = datetime.now()
        print(local_path)
        review_info = agent.check_assignments_gemini(directory=local_path)
        if review_info is None:
            return
        end_time = datetime.now()
        review_ai, details = review_manager.create_ai_review_info(request_id, review_info)
        if review_ai is None or details is None:
            return
        review_ai.start_time = start_time
        review_ai.end_time = end_time
        try:
            Session = sessionmaker(bind=engine, autoflush=False,)
            with Session() as session:
                session.add(review_ai)
                for detail in details:
                    session.add(detail)
                session.commit()
        except Exception (e):
            print(e)
        finally:
            session.close()

        try:
            shutil.rmtree(local_path)
            logger.debug(f"{local_path} deleted.")
        except OSError as e:
            print(f"Error deleting directory {local_path}: {e}")


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



