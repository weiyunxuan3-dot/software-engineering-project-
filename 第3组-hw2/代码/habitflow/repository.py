import sqlite3
from datetime import date
from models import Habit, DailyRecord

DB_PATH = "habitflow.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            target_days INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status INTEGER NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    ''')
    conn.commit()
    conn.close()

def get_all_habits():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, frequency, target_days FROM habits")
    rows = c.fetchall()
    conn.close()
    return [Habit(id=r[0], name=r[1], frequency=r[2], target_days=r[3]) for r in rows]

def add_habit(name, frequency, target_days):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO habits (name, frequency, target_days) VALUES (?, ?, ?)",
              (name, frequency, target_days))
    conn.commit()
    conn.close()

def get_today_record(habit_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute("SELECT id, status FROM daily_records WHERE habit_id=? AND date=?", (habit_id, today))
    row = c.fetchone()
    conn.close()
    if row:
        return DailyRecord(id=row[0], habit_id=habit_id, date=date.today(), status=bool(row[1]))
    return None

def check_in(habit_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = date.today().isoformat()
    # 检查是否已打卡
    c.execute("SELECT id FROM daily_records WHERE habit_id=? AND date=?", (habit_id, today))
    if c.fetchone():
        conn.close()
        return False  # 已打卡
    c.execute("INSERT INTO daily_records (habit_id, date, status) VALUES (?, ?, 1)",
              (habit_id, today))
    conn.commit()
    conn.close()
    return True
