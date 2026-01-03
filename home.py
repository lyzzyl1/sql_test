# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
import os
from supabase import create_client, Client

st.set_page_config(page_title="跑步模拟系统", layout="wide", page_icon="🏃")


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

st.title("科学推理能力测试")
st.markdown("---")

# 欢迎信息
st.header("科学推理能力测试")
st.write("""
## 本测试通过创设一系列科学情境，测试您的科学推理能力。

""")
# 添加用户名输入
user_name = st.text_input("👤 请输入您的姓名", "")
if user_name:
     st.session_state.user_name = user_name


# 显示两个题目链接
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 开始测试")
    if st.button("前往第一题", use_container_width=True):
        st.session_state.history = []
        st.switch_page("pages/q1.py")


