from repository import get_all_habits, add_habit, check_in, get_today_record

def list_habits():
    return get_all_habits()

def create_habit(name, frequency="daily", target_days=30):
    add_habit(name, frequency, target_days)

def do_check_in(habit_id):
    return check_in(habit_id)

def get_today_status(habit_id):
    record = get_today_record(habit_id)
    return record.status if record else False