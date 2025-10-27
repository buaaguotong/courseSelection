import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="学生选课系统", page_icon="🎓", layout="centered")

# 初始化课程
if "courses" not in st.session_state:
    st.session_state.courses = {
        "时段A（周一上午）": 0,
        "时段B（周一下午）": 0,
        "时段C（周二上午）": 0,
        "时段D（周二下午）": 0,
        "时段E（周三上午）": 0
    }

st.title("🎓 学生选课系统")
st.write("每个时段限额 60 人，先到先得。已满课程将无法选择。")

# 输入信息
name = st.text_input("姓名")
sid = st.text_input("学号")
phone = st.text_input("手机号")

# 显示课程选项
selected_course = st.radio("请选择一个课程时段：",
    options=list(st.session_state.courses.keys()),
    key="selected_course"
)

if st.button("确认选课"):
    if not name or not sid or not phone:
        st.warning("请填写完整信息后再提交！")
    else:
        # 获取当前课程人数
        current_count = st.session_state.courses[selected_course]
        if current_count >= 60:
            st.error("该课程已满，请选择其他时段。")
        else:
            # 增加选课人数
            st.session_state.courses[selected_course] += 1

            # 写入文件
            record = pd.DataFrame([{
                "姓名": name,
                "学号": sid,
                "手机号": phone,
                "选课时段": selected_course,
                "提交时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            record.to_csv("record.csv", mode="a", index=False, header=False, encoding="utf-8-sig")

            st.success(f"选课成功！你选择的是：{selected_course}")
            st.balloons()

# 显示实时选课人数
st.subheader("📊 当前各时段报名人数")
df = pd.DataFrame(
    [{"课程": k, "已选人数": v, "剩余额度": 60 - v} for k, v in st.session_state.courses.items()]
)
st.table(df)
