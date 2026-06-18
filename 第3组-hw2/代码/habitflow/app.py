import streamlit as st
from services import list_habits, create_habit, do_check_in, get_today_status
from repository import init_db

init_db()

st.set_page_config(page_title="HabitFlow", layout="centered")
st.title("📊 HabitFlow 个人习惯追踪器")

# 侧边栏：创建习惯
with st.sidebar:
    st.subheader("✨ 创建新习惯")
    habit_name = st.text_input("习惯名称")
    target_days = st.number_input("目标天数", min_value=1, max_value=365, value=30)
    if st.button("添加习惯") and habit_name:
        create_habit(habit_name, target_days=target_days)
        st.success(f"已添加习惯：{habit_name}")
        st.rerun()

# 主界面：显示今日习惯列表
st.subheader("📋 今日待打卡")

habits = list_habits()
if not habits:
    st.info("还没有习惯，在左侧添加一个吧！")
else:
    for habit in habits:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{habit.name}** (目标{habit.target_days}天)")
        with col2:
            status = get_today_status(habit.id)
            if status:
                st.success("✅ 已打卡")
            else:
                st.warning("⏳ 待打卡")
        with col3:
            if not status:
                if st.button("打卡", key=f"check_{habit.id}"):
                    if do_check_in(habit.id):
                        st.success("🎉 打卡成功！")
                        st.rerun()
                    else:
                        st.error("打卡失败")

# 统计信息
st.subheader("📈 数据摘要")
total = len(habits)
done = sum(1 for h in habits if get_today_status(h.id))
st.metric("今日完成率", f"{done}/{total}")