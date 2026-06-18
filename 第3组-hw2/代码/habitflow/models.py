from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Habit:
    id: Optional[int]
    name: str
    frequency: str  # "daily"
    target_days: int

@dataclass
class DailyRecord:
    id: Optional[int]
    habit_id: int
    date: date
    status: bool  # True=已完成