import threading
from typing import Optional, Callable
from datetime import datetime
import logging
from queue import Queue
import time
from enum import Enum

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
        self.event = threading.Event()  # 用于同步等待任务完成

class QueueTaskManager:
    """
        管理队列任务，每次只执行一个
    """

    def __init__(self, task_executor: Optional[Callable]):
        self._lock = threading.Lock()
        self._is_generating = False
        self._current_task: Optional[GenerationTask] = None
        self._task_queue = Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._task_results = {}  # 存储任务结果
        self.logger = logging.getLogger(__name__)
        self.task_executor = task_executor


    def start_worker(self):
        """启动工作线程"""
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._worker_thread = threading.Thread(target=self._process_queue, daemon=True)
            self._worker_thread.start()

    def _process_queue(self):
        """处理队列中的任务"""
        while True:
            try:
                if not self._task_queue.empty():
                    with self._lock:
                        if not self._is_generating:
                            self._is_generating = True
                            task = self._task_queue.get()
                            self._current_task = task
                            task.status = TaskStatus.PROCESSING
                            self._execute_task(task)
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error processing task: {str(e)}")
                # self._reset_state()

    def _execute_task(self, task: GenerationTask):
        """执行具体的生成任务"""
        try:
            self.logger.info(f"开始生成题目: {task.task_id}")
            # 这里调用实际的题目生成方法
            result = self.task_executor(task)
            task.status = TaskStatus.COMPLETED
            task.result = result
            self._notify_task_completion(task)
        except Exception as e:
            self.logger.error(f"生成题目失败: {str(e)}")
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            self._notify_task_failure(task)
        finally:
            task.event.set()  # 通知任务已完成
            # self._reset_state()

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

    def add_generation_task(self, subject: str, student_id: int, knowledge_points: list, 
                          callback: Optional[Callable] = None, wait: bool = False) -> str:
        """
        添加题目生成任务
        
        Args:
            subject: 学科
            student_id: 学生ID
            knowledge_points: 知识点列表
            callback: 回调函数，接收 GenerationTask 对象作为参数
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
        
        try:
            self._task_queue.put(task)
            self.start_worker()
            
            if wait:
                # 等待任务完成
                task.event.wait()
                if task.status == TaskStatus.FAILED:
                    raise Exception(f"Task failed: {task.error_message}")
                
            return task_id
        except Exception as e:
            self.logger.error(f"添加任务失败: {str(e)}")
            raise

    def get_task_status(self, task_id: str) -> Optional[dict]:
        """获取任务状态"""
        tasks = list(self._task_queue.queue)
        if self._current_task and self._current_task.task_id == task_id:
            task = self._current_task
        else:
            task = next((t for t in tasks if t.task_id == task_id), None)
            
        if task:
            return {
                'task_id': task.task_id,
                'status': task.status.value,
                'error_message': task.error_message,
                'created_at': task.created_at
            }
        return None