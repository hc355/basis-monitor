import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ========= 页面基础设置 =========
st.set_page_config(page_title="热卷HC+355带钢基差监控", layout="wide")

# ========= 登录模块 =========
if "login_ok" not in st.session_state:
    st.session_state.login_ok = False

if not st.session_state.login_ok:
    st.title("🔒 登录验证｜基差监控系统")
    password_input = st.text_input("请输入访问密码", type="password")
    if st.button("登录系统"):
        # 在这里修改你的登录密码
        if password_input == "961896372":
            st.session_state.login_ok = True
            st.rerun()
        else:
            st.error("密码错误，请重新输入！")
    st.stop()

# ========= 主监控页面 =========
st.title("🔥热卷HC盘面 + 355带钢现货 | 基差实时监控")
st.subheader("基差公式：基差 = 355带钢现货价 − 热卷主力盘面价")

# 定义csv文件名
csv_file = "basis_record.csv"

# 如果文件不存在，新建空csv
if not os.path.exists(csv_file):
    df_empty = pd.DataFrame(columns=["record_time", "hc_price", "spot_price", "basis"])
    df_empty.to_csv(csv_file, index=False)

# 读取历史数据
df = pd.read_csv(csv_file)

# 价格输入框
spot_price = st.number_input("请输入【355带钢现货价格】元/吨", value=2815, step=1)
hc_price = st.number_input("请输入【热卷HC主力盘面价格】元/吨", value=2800, step=1)

# 计算基差
basis = spot_price - hc_price
st.info(f"✅ 当前计算基差：{basis:.2f} 元/吨")

# 保存记录按钮
if st.button("采集行情，保存本次基差记录"):
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_row = pd.DataFrame([[now_time, hc_price, spot_price, basis]],
                           columns=["record_time", "hc_price", "spot_price", "basis"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("✅ 记录保存成功！")

# 绘制历史走势图
if len(df) > 0:
    fig = px.line(df, x="record_time", y=["hc_price", "spot_price", "basis"],
                  labels={"value": "价格(元/吨)", "variable": "指标"},
                  title="历史：热卷盘面 / 355带钢现货 / 基差走势")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)
    # 导出csv下载按钮（重点！用来备份你的全部基差数据）
    csv_download = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 下载全部基差记录CSV备份",
        data=csv_download,
        file_name="基差历史记录.csv",
        mime="text/csv"
    )
else:
    st.info("暂无历史数据，点击上方【采集行情】生成第一条记录")

# 登出按钮
if st.button("🔓 退出登录"):
    st.session_state.login_ok = False
    st.rerun()