import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from supabase import create_client, Client

st.set_page_config(page_title="第三题 - 生态金字塔", layout="wide")

# ========== 数据库连接部分 ==========
@st.cache_resource
def init_connection() -> Client:
    """创建Supabase客户端"""
    # 🔥 修改这里的值为您的实际值！ 🔥
    url = "https://fmritvcqvyhdxdjzxykl.supabase.co"  # 从图片获取的项目URL
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZtcml0dmNxdnloZHhkanp4eWtsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzM2MzU1OCwiZXhwIjoyMDgyOTM5NTU4fQ.7oer9psAEBQdkbNJmiI6C5fthH-Np3tO5-xK1D7kLP8"  # 需要在Supabase设置->API中找到

    url = os.environ.get("SUPABASE_URL", url)
    key = os.environ.get("SUPABASE_KEY", key)
    
    if not url or not key:
        st.error("请配置Supabase连接信息！")
        return None
    
    try:
        supabase = create_client(url, key)
        st.success("✅ 数据库连接成功！")
        return supabase
    except Exception as e:
        st.error(f"❌ 数据库连接失败: {e}")
        return None

def save_simulation_data_to_supabase(user_name, q_id, answer, history):
    """保存数据到Supabase"""
    supabase = init_connection()
    if not supabase:
        return False
    
    try:
        data = {
            "user_name": user_name,
            "answer": answer,
            "q_id": q_id ,
            "history_data": json.dumps(str(history), ensure_ascii=False)
        }
        
        response = supabase.table("test_records").insert(data).execute()
        
        if response.data:
            return True
        else:
            st.error(f"保存失败: {response.error}")
            return False
    except Exception as e:
        st.error(f"保存到数据库时出错: {e}")
        return False

# 在每个页面的开头都添加
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("第三题：生态系统中的能量流动分析")
st.markdown("---")

# 1. 题干文字
st.markdown("""
### 题目描述

在一个封闭的森林生态系统中，科学家观察到了以下食物链关系：

1. **生产者**：绿色植物（通过光合作用产生能量）
2. **初级消费者**：草食动物（如兔子、鹿）
3. **次级消费者**：肉食动物（如狐狸、狼）
4. **分解者**：真菌和细菌

### 问题

1. 解释为什么能量在食物链中逐级递减
2. 如果这个森林生态系统被开发，会如何影响能量流动？

请根据生态学原理，详细分析上述问题。
""")

# 2. 图片
st.subheader("🔬 生态系统能量金字塔示意图")


# 3. 用户回答的文本框
st.subheader("📝 请在此输入您的分析回答")

# 使用 st.session_state.history 保存用户输入

# 大文本框供用户输入回答
answer = st.text_area(
    "请详细阐述您的分析和计算过程：",
    value=st.session_state.history,
    height=300,
)

# 实时保存用户输入
st.session_state.history = answer


#提交按钮
col_submit = st.columns([1])[0]
with col_submit:
    submit_button = st.button("✅ 提交答案",  type="primary",)
    # 处理提交按钮点击
if submit_button:
    if save_simulation_data_to_supabase(st.session_state.user_name,3,st.session_state.history,st.session_state.history):#题号！
        st.success("✅ 数据已成功保存到后台！")

# 页面底部导航
st.markdown("---")
col_left,col_mid, col_right = st.columns(3)
with col_left:
    if st.button("⬅️返回主页", use_container_width=True):
        st.session_state.history = []
        st.switch_page("home.py")
with col_mid:
    if st.button("⬅️ 上一题", use_container_width=True):
        st.session_state.history = []
        st.switch_page("pages/q2.py")
with col_right:
    if st.button("下一题 ➡️", use_container_width=True):
        st.session_state.history = []

        st.switch_page("pages/q3.py")
