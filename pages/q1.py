import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
from supabase import create_client, Client

st.set_page_config(page_title="第一题 - 跑步模拟", layout="wide")

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
st.title("第一题：跑步健康风险模拟")


st.markdown("---")

# 左侧栏 - 输入控件
with st.sidebar:
    st.header("跑步模拟设置")
    
    temp = st.slider("空气温度 (°C)", 20, 40, 25, step=5, help="选择跑步时的环境温度")
    humidity = st.slider("空气湿度 (%)", 10, 90, 40, step=20, help="选择跑步时的环境湿度")
    

    water = st.selectbox("是否喝水", ["是", "否"], help="跑步过程中是否补充水分")
    
    st.markdown("---")
    run_button = st.button("开始模拟", type="primary", use_container_width=True)


# 主界面
col1, col2=st.columns([1,2])  #两列宽度比

with col1:
    st.header("📝 问题描述")
    st.write("在炎热干燥天气下（气温40°C，湿度20%）跑步1小时不喝水，会遇到什么健康危险？")
    
    answer = st.selectbox(
        "选择健康危险:",
        ["无危险", "脱水 (Dehydration)", "中暑 (Heat Stroke)", "热衰竭 (Heat Exhaustion)", "低温症 (Hypothermia)"]
    ) #下拉选择框
    
    if answer:#绿色成功提示框
        st.success(f"您选择了: **{answer}**")

with col2:
    if run_button:#如果按了该按钮
        #开始模拟计算
        # 简化计算逻辑
        sweat = round(0.5 + (temp - 20) * 0.1, 1)
        water_loss = round(sweat * 0.7 + (-0.3 if water == "是" else 0), 1)
        body_temp = round(37 + (temp - 25) * 0.1 + (water_loss * 0.05 if water == "否" else 0), 1)
                
        # 建立图表
        data = pd.DataFrame({
            "指标": ["温度", "湿度", "出汗量", "水分流失", "体温"],
            "值": [temp, humidity, sweat, water_loss, body_temp]
        })
                     
        st.session_state.history.append({
            "温度": temp, "湿度": humidity, "喝水": water,
            "出汗量": sweat, "水分流失": water_loss, "体温": body_temp
        })
    
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
    if save_simulation_data_to_supabase(st.session_state.user_name,1,answer,st.session_state.history):#题号！
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
        st.switch_page("pages/q2.py")