from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Callable
from datetime import datetime
import logging
import time
from enum import Enum
import threading

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GenerationTask:
    def __init__(self, task_id: str, subject: str, student_id: int, knowledge_points: list, 
                 callback: Optional[Callable] = None):
        self.task_id = task_id
        self.subject = subject
        self.student_id = student_id
        self.knowledge_points = knowledge_points
        self.status = TaskStatus.PENDING
        self.error_message = None
        self.created_at = datetime.now()
        self.callback = callback
        self.event = threading.Event()
        self.result = None

class ConcurrentTaskManager:
    """
    支持多线程并发的题目生成器
    """
    def __init__(self, max_workers: int = 3):
        """
        初始化生成器
        Args:
            max_workers: 最大并发线程数
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._tasks = {}  # 存储所有任务
        self._lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def _generate_questions(self, task: GenerationTask):
        """
        实际的题目生成方法，需要根据实际情况实现
        """
        try:
            # 模拟生成过程
            self.logger.info(f"Generating questions for task {task.task_id}")
            time.sleep(5)  # 模拟耗时操作
            # 这里添加实际的题目生成逻辑
            return {"generated": True, "questions": []}
        except Exception as e:
            self.logger.error(f"Question generation failed: {str(e)}")
            raise

    def _execute_task(self, task: GenerationTask):
        """执行任务的包装方法"""
        try:
            task.status = TaskStatus.PROCESSING
            result = self._generate_questions(task)
            task.result = result
            task.status = TaskStatus.COMPLETED
            self._notify_task_completion(task)
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            self._notify_task_failure(task)
        finally:
            task.event.set()

    def _notify_task_completion(self, task: GenerationTask):
        """通知任务完成"""
        if task.callback:
            try:
                task.callback(task)
            except Exception as e:
                self.logger.error(f"Error in completion callback: {str(e)}")

    def _notify_task_failure(self, task: GenerationTask):
        """通知任务失败"""
        if task.callback:
            try:
                task.callback(task)
            except Exception as e:
                self.logger.error(f"Error in failure callback: {str(e)}")

    def submit_task(self, subject: str, student_id: int, knowledge_points: list,
                   callback: Optional[Callable] = None, wait: bool = False) -> str:
        """
        提交生成任务
        
        Args:
            subject: 学科
            student_id: 学生ID
            knowledge_points: 知识点列表
            callback: 回调函数
            wait: 是否等待任务完成
            
        Returns:
            str: task_id
        """
        task_id = f"task_{int(time.time())}_{student_id}"
        task = GenerationTask(
            task_id=task_id,
            subject=subject,
            student_id=student_id,
            knowledge_points=knowledge_points,
            callback=callback
        )
        
        with self._lock:
            self._tasks[task_id] = task
        
        # 提交任务到线程池
        future = self.executor.submit(self._execute_task, task)
        
        if wait:
            # 等待任务完成
            task.event.wait()
            if task.status == TaskStatus.FAILED:
                raise Exception(f"Task failed: {task.error_message}")
            return task.result
            
        return task_id

    def get_task_status(self, task_id: str) -> Optional[dict]:
        """获取任务状态"""
        task = self._tasks.get(task_id)
        if task:
            return {
                'task_id': task.task_id,
                'status': task.status.value,
                'error_message': task.error_message,
                'created_at': task.created_at,
                'result': task.result if task.status == TaskStatus.COMPLETED else None
            }
        return None

    def get_running_tasks(self) -> list:
        """获取正在运行的任务列表"""
        return [
            task_id for task_id, task in self._tasks.items()
            if task.status == TaskStatus.PROCESSING
        ]

    def shutdown(self):
        """关闭生成器"""
        self.executor.shutdown(wait=True)

# 使用示例
def handle_task_result(task: GenerationTask):
    """处理任务结果的回调函数"""
    if task.status == TaskStatus.COMPLETED:
        print(f"Task {task.task_id} completed successfully!")
        print(f"Result: {task.result}")
    else:
        print(f"Task {task.task_id} failed: {task.error_message}")

if __name__ == "__main__":
    # 创建一个最多支持3个并发的生成器
    generator = ConcurrentTaskManager(max_workers=3)
    
    # 提交多个任务
    tasks = [
        {
            "subject": "math",
            "student_id": i,
            "knowledge_points": ["函数", "方程"],
        }
        for i in range(5)  # 创建5个任务
    ]
    
    # 异步提交所有任务
    task_ids = []
    for task in tasks:
        task_id = generator.submit_task(
            subject=task["subject"],
            student_id=task["student_id"],
            knowledge_points=task["knowledge_points"],
            callback=handle_task_result
        )
        task_ids.append(task_id)
        print(f"Submitted task: {task_id}")
    
    # 监控任务状态
    while task_ids:
        for task_id in task_ids[:]:  # 使用切片创建副本以便在循环中修改列表
            status = generator.get_task_status(task_id)
            if status and status['status'] in ['completed', 'failed']:
                print(f"Task {task_id} finished with status: {status['status']}")
                task_ids.remove(task_id)
        
        if task_ids:
            print(f"Still running: {len(task_ids)} tasks")
            time.sleep(1)
    
    # 关闭生成器
    generator.shutdown()