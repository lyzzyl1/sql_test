import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from supabase import create_client, Client
import math
import random

st.set_page_config(page_title="第二题 - 单摆探究", layout="wide")

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

# 页面标题
st.title("第二题：单摆周期影响因素")


# 左侧栏 - 输入控件
with st.sidebar:
    st.header("单摆实验设置")
    
    m = st.slider("小球质量 (g)", 50, 100, 80, step=10, help="选择小球质量")
    l = st.slider("摆线长度 (cm)", 10, 50, 30, step=10, help="选择摆线长度")
    a = st.slider("摆动角度 (°)", 3, 10, 5, step=1, help="选择初始摆动角度")
    
    st.markdown("---")
    run_button = st.button("开始模拟", type="primary", use_container_width=True)

# 主界面
col1, col2=st.columns([1,2])  #两列宽度比

with col1:
    st.header("📝 问题描述")
    st.write("小明在探究单摆的摆动周期与哪些因素有关，请你进行实验挖掘规律。")
    
    answer = st.selectbox(
        "有关因素:",
        ["小球质量", "摆线长度", "摆动角度", "无"]
    ) #下拉选择框
    
    if answer:#绿色成功提示框
        st.success(f"您选择了: **{answer}**")

with col2:
    if run_button:#如果按了该按钮
        
        #开始模拟计算
        # 简化计算逻辑
        time = round( 2*math.pi*math.sqrt(l/9.78)+random.uniform(-0.2, 0.2) ,2)
         
        # 建立图表
        data = pd.DataFrame({
            "指标": ["小球质量", "摆线长度", "摆动角度", "单摆周期"],
            "值": [m, l, a, time]
        })
                
        st.session_state.history.append({
            "小球质量":m, "摆线长度":l, "摆动角度":a, "单摆周期":time
        })
    
    # 历史记录
    if "history" not in st.session_state:
        st.session_state.history = []
    st.header("📊 模拟结果")    
    if "history" in st.session_state:#如果非空
        st.subheader("📈 数据记录")
        df = pd.DataFrame(st.session_state.history[-5:])  # 显示最近5次
        st.dataframe(df)

#提交按钮
col_submit = st.columns([1])[0]
with col_submit:
    submit_button = st.button("✅ 提交答案",  type="primary",)
    # 处理提交按钮点击
if submit_button:
    if save_simulation_data_to_supabase(st.session_state.user_name,2,answer,st.session_state.history):#题号！
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
        st.switch_page("pages/q1.py")
with col_right:
    if st.button("下一题 ➡️", use_container_width=True):
        st.session_state.history = []
        st.switch_page("pages/q3.py")