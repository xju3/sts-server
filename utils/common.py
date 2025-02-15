import base64
from pydantic import BaseModel
from PIL import Image
import matplotlib.pyplot as plt
import uuid

import json
from typing import Protocol


def generate_uuid():
    return str(uuid.uuid1())

class JsonSerializable(Protocol):
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return self.to_json()
    
def encode_image(image_path):
    """Convert image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

from datetime import datetime, timedelta


def get_date_from_week_id(year_id: int, week_id: int):
    """
    根据年份ID和周ID获取该周的起始日期和结束日期（以周日为一周的开始）。

    Args:
        year_id (int): 年份
        week_id (int): 周数 (1-53)

    Returns:
        tuple: (week_start, week_end)
        - week_start: 指定周的周日 00:00:00
        - week_end: 下一周的周日 00:00:00 (不包含在指定周范围内)
    """
    # 计算该年的第一个周日的日期
    first_day_of_year = datetime(year_id, 1, 1)
    days_to_first_sunday = (6 - first_day_of_year.weekday()) % 7
    first_sunday = first_day_of_year + timedelta(days=days_to_first_sunday)

    # 计算目标周的周日
    target_week_sunday = first_sunday + timedelta(weeks=(week_id - 1))
    target_week_sunday = target_week_sunday.replace(hour=0, minute=0, second=0, microsecond=0)

    # 计算下一周的周日
    next_week_sunday = target_week_sunday + timedelta(days=7)

    return target_week_sunday, next_week_sunday



def get_week_dates(delta: int):
    """
    获取指定周的起始日期和结束日期（以周日为一周的开始）
    
    Args:
        delta (int): 0表示本周，-1表示上周，以此类推。
    
    Returns:
        tuple: (week_start, week_end)
        - week_start: 指定周的周日 00:00:00
        - week_end: 下一周的周日 00:00:00 (不包含在指定周范围内)
    """
    today = datetime.now()
    
    # 获取本周日的日期
    # weekday()返回0-6（周一到周日），所以需要调整计算方式
    days_since_sunday = (today.weekday() + 1) % 7  # 转换为以周日为0的计数
    this_week_sunday = today - timedelta(days=days_since_sunday)
    # 将时间设置为当天的 00:00:00
    this_week_sunday = this_week_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # 根据delta计算指定周的周日
    target_week_sunday = this_week_sunday + timedelta(days=7 * delta)
    # 指定周结束时间就是下周日凌晨
    next_week_sunday = target_week_sunday + timedelta(days=7)

    return target_week_sunday, next_week_sunday


def get_week_ids(delta: int):
    """
    获取指定周的年份ID和周ID（以周日为一周的开始）
    
    Args:
        delta (int): 0表示本周，-1表示上周，以此类推。
    
    Returns:
        tuple: (year_id, week_id)
        - year_id: 年份
        - week_id: 周数 (1-53)
    """
    today = datetime.now()
    
    # 获取当前是一周的第几天（以周日为0）
    days_since_sunday = (today.weekday() + 1) % 7
    
    # 获取本周日的日期
    this_week_sunday = today - timedelta(days=days_since_sunday)
    
    # 获取目标周日的日期
    target_week_sunday = this_week_sunday + timedelta(days=7 * delta)
    
    # 使用 strftime 获取年份和周数
    # %U: 一年中的第几周（00-53），以周日为每周的第一天
    year_id = target_week_sunday.year
    week_id = int(target_week_sunday.strftime("%U"))
    
    # 处理跨年的特殊情况
    if week_id == 0:
        # 如果是第0周（年初的不完整周），则应该算作上一年的最后一周
        target_week_sunday = target_week_sunday - timedelta(days=7)
        year_id = target_week_sunday.year
        week_id = int(target_week_sunday.strftime("%U"))

    return year_id, week_id