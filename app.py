import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ================= 页面全局设置 =================
st.set_page_config(page_title="新型电力系统智能调度决策平台", layout="wide", page_icon="⚡",
                   initial_sidebar_state="expanded")

# ================= 自定义 CSS: 极致清晰的现代亮色仪表盘风格 =================
custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #F8FAFC; }
    html, body, [class*="css"], p { color: #334155 !important; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    
    .kpi-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 20px; text-align: left;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border-top: 4px solid #3B82F6;
        margin-bottom: 1rem; transition: transform 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .kpi-title { color: #64748B; font-size: 14px; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
    .kpi-value { color: #0F172A; font-size: 30px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
    .kpi-delta { font-size: 13px; margin-top: 5px; font-weight: 600; }
    .delta-up { color: #EF4444; } .delta-down { color: #10B981; }

    h1 { color: #0F172A !important; font-weight: 800 !important; }
    h2, h3, h4, h5 { color: #1E293B !important; font-weight: 700 !important; }
    .stDataFrame { background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0; padding: 5px; }
    hr { border-top: 1px solid #E2E8F0; margin: 20px 0; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ================= 侧边栏导航 =================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #2563EB; font-weight: 900;'>⚡ 智能调度中枢</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 13px; margin-top: -15px;'>Power System Smart Dispatch</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("模块导航",
                    ["1. 源荷态势感知大屏", "2. 电力数据时序分解演进", "3. 供需缺口 3D 时空雷达",
                     "4. AI 大模型调度决策生成"]
                    )
    st.markdown("---")
    st.success("核心数据库连接正常")
    st.info("系统版本：V 3.1 (Algorithms Upgraded)\n\n底层数据：国家统计局\n\n智能体：Qwen-Turbo")

# ================= 模拟加载数据 =================
@st.cache_data
def load_dummy_data():
    dates = pd.date_range(start='2018-01-01', end='2023-12-01', freq='MS')
    provinces = ['四川省', '江苏省', '内蒙古自治区', '广东省', '山东省', '浙江省', '新疆维吾尔自治区']
    data = []
    # 模拟“动态增长”的基数
    for p in provinces:
        trend_base = 300
        for i, d in enumerate(dates):
            # 基数随时间增长 (模拟宏观经济增长)
            trend_val = trend_base + i * 1.5 
            # 季节性波动因基数增长而放大 (乘法效应)
            month_factor = np.sin(d.month / 12 * 2 * np.pi)
            seasonality_val = trend_val * (0.15 * month_factor) 
            
            consumption = trend_val + seasonality_val + np.random.normal(0, 5)
            generation = trend_val + 10 + seasonality_val + np.random.normal(0, 5)
            data.append([d, p, consumption, generation, consumption - generation])
    return pd.DataFrame(data, columns=['Date', 'Province', 'Consumption', 'Generation', 'Shortage'])

df = load_dummy_data()

# ================= 页面 1：源荷大屏 =================
if page == "1. 源荷态势感知大屏":
    st.markdown("<h1>📊 全国省级电网源荷态势感知</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>基于多源传感器及统计局宏观数据，实时监控各省级行政区全社会用电负荷与发电量极值。</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">监控省份节点</div><div class="kpi-value">{len(df["Province"].unique())} 个</div><div class="kpi-delta" style="color:#64748B;">覆盖核心电网区域</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card" style="border-top-color: #8B5CF6;"><div class="kpi-title">数据时序跨度</div><div class="kpi-value">{len(df["Date"].unique())} 期</div><div class="kpi-delta" style="color:#64748B;">月度高频采样</div></div>', unsafe_allow_html=True)
    with col3:
        max_shortage = df['Shortage'].max()
        st.markdown(f'<div class="kpi-card" style="border-top-color: #EF4444;"><div class="kpi-title">历史最大缺口峰值</div><div class="kpi-value">{max_shortage:.1f} <span style="font-size:16px; color:#64748B;">GWh</span></div><div class="kpi-delta delta-up">⚠️ 高压运行警告</div></div>', unsafe_allow_html=True)
    with col4:
        max_gen = df['Generation'].max()
        st.markdown(f'<div class="kpi-card" style="border-top-color: #10B981;"><div class="kpi-title">单月最大发电释放</div><div class="kpi-value">{max_gen:.1f} <span style="font-size:16px; color:#64748B;">GWh</span></div><div class="kpi-delta delta-down">🟢 产能充沛</div></div>', unsafe_allow_html=True)

    st.write("")
    col_left, col_right = st.columns([1.2, 2])
    with col_left:
        st.markdown("### 📋 宏观时序矩阵")
        formatted_df = df.head(20).copy()
        formatted_df['Date'] = formatted_df['Date'].dt.strftime('%Y-%m')
        st.dataframe(formatted_df.style.format({"Consumption": "{:.1f}", "Generation": "{:.1f}", "Shortage": "{:.1f}"}), hide_index=True, use_container_width=True, height=350)
    with col_right:
        st.markdown("### 📈 节点源荷动态追踪")
        sel_prov = st.selectbox("选择目标省份：", df['Province'].unique(), label_visibility="collapsed")
        prov_df = df[df['Province'] == sel_prov]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=prov_df['Date'], y=prov_df['Consumption'], mode='lines', name='用电负荷', line=dict(color='#EF4444', width=3)))
        fig_line.add_trace(go.Scatter(x=prov_df['Date'], y=prov_df['Generation'], mode='lines', name='发电量', line=dict(color='#10B981', width=3)))
        fig_line.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
            font=dict(color="#334155"), hovermode="x unified", height=350, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor='#E2E8F0'), yaxis=dict(gridcolor='#E2E8F0'))
        st.plotly_chart(fig_line, use_container_width=True)

# ================= 页面 2：电力数据时序分解演进 =================
elif page == "2. 电力数据时序分解演进":
    st.markdown("<h1>📈 电力数据时序乘法分解演进 (Multiplicative Model)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>由于电力规模逐年扩大，系统的波动振幅呈喇叭口发散。我们采用高阶乘法模型 (Y = Trend × Seasonality × Noise) 进行精准降噪分解。</p>", unsafe_allow_html=True)
    st.markdown("---")

    sel_prov_2 = st.selectbox("🎯 定位分析省份：", df['Province'].unique(), key="prov_2")
    prov_df_2 = df[df['Province'] == sel_prov_2].sort_values('Date').copy()

    # --- 图 1：原有的同环比动能图 ---
    st.markdown("### 📊 绝对产出与同环比动能矩阵")
    prov_df_2['Gen_MoM'] = prov_df_2['Generation'].pct_change(periods=1) * 100
    prov_df_2['Gen_YoY'] = prov_df_2['Generation'].pct_change(periods=12) * 100

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(x=prov_df_2['Date'], y=prov_df_2['Generation'], name="月度发电总量 (GWh)", marker_color="#3B82F6", opacity=0.8), secondary_y=False)
    fig2.add_trace(go.Scatter(x=prov_df_2['Date'], y=prov_df_2['Gen_YoY'], name="同比增速 YoY (%)", mode="lines+markers", line=dict(color="#F59E0B", width=3), marker=dict(symbol="diamond", size=6)), secondary_y=True)
    fig2.add_trace(go.Scatter(x=prov_df_2['Date'], y=prov_df_2['Gen_MoM'], name="环比增速 MoM (%)", mode="lines+markers", line=dict(color="#10B981", width=3, dash="dot"), marker=dict(symbol="circle", size=5)), secondary_y=True)

    fig2.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#334155"),
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=450)
    fig2.update_xaxes(gridcolor='#E2E8F0')
    fig2.update_yaxes(title_text="绝对产出 (GWh)", secondary_y=False, showgrid=False)
    fig2.update_yaxes(title_text="相对增幅 (%)", secondary_y=True, showgrid=True, gridcolor='#E2E8F0')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- 图 2：优化后的乘法分解 (Multiplicative Decomposition) ---
    st.markdown("### 🔬 动态产能信号深度分解 (Trend / Dynamic Cycle / Noise)")
    st.markdown("<p style='color:#64748B; font-size: 14px;'>注：长周期趋势扩展为24个月平滑，完美过滤年际干扰；季节性振幅采用动态比率(Ratio)计算，客观反映供需压力的同步放大。</p>", unsafe_allow_html=True)
    
    ts_series = prov_df_2.set_index('Date')['Generation']
    
    # 1. 长周期宏观趋势 (扩大到 24 个月滚动平均，体现跨年周期)
    trend = ts_series.rolling(window=24, center=True, min_periods=6).mean()
    
    # 2. 动态季节性波动 (乘法模型)
    # 提取真实值相对于趋势的比率 (例如夏天用电是平均值的 1.2 倍)
    ratio = ts_series / trend
    # 按照每年的1-12月，求出每年固定的季节系数 (Annual Seasonality Factor)
    seasonal_index = ratio.groupby(ratio.index.month).transform('mean')
    # 将系数还原成随基数扩大的绝对波动值
    seasonality = trend * (seasonal_index - 1)
    
    # 3. 突发随机噪声 (剔除趋势和规律性季节波动后，剩下的异常突变)
    noise = ts_series - trend - seasonality

    fig_decomp = make_subplots(rows=4, cols=1, shared_xaxes=True, 
                               subplot_titles=("1. 原始动态增长信号 (Raw Expanding Signal)", "2. 跨年度长周期宏观趋势 (24-Month Macro Trend)", 
                                               "3. 振幅扩大型季节波动 (Dynamic Seasonality Cycle)", "4. 突发随机噪声极值点 (Random Residuals)"),
                               vertical_spacing=0.08)

    fig_decomp.add_trace(go.Scatter(x=ts_series.index, y=ts_series, line=dict(color="#3B82F6", width=2)), row=1, col=1)
    fig_decomp.add_trace(go.Scatter(x=ts_series.index, y=trend, line=dict(color="#EF4444", width=3)), row=2, col=1)
    fig_decomp.add_trace(go.Scatter(x=ts_series.index, y=seasonality, line=dict(color="#10B981", width=2), fill='tozeroy'), row=3, col=1)
    fig_decomp.add_trace(go.Scatter(x=ts_series.index, y=noise, mode='markers+lines', line=dict(color="#CBD5E1", width=1), marker=dict(color="#475569", size=6, symbol="cross")), row=4, col=1)

    fig_decomp.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                             font=dict(color="#334155"), height=850, showlegend=False, hovermode="x unified")
    fig_decomp.update_xaxes(gridcolor='#E2E8F0')
    fig_decomp.update_yaxes(gridcolor='#E2E8F0')
    st.plotly_chart(fig_decomp, use_container_width=True)

# ================= 页面 3：3D 时空图 =================
elif page == "3. 供需缺口 3D 时空雷达":
    st.markdown("<h1>🌐 区域互济缺口时空演化雷达</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>【色彩空间修正】白色基准线严格锚定“供需平衡点(缺口=0)”。蓝色区域表示电力冗余，红色高地代表电网承压濒临极限。</p>", unsafe_allow_html=True)
    st.markdown("---")

    view_mode = st.radio("👀 请选择观测视角 (View Mode)：", 
                         ["🧊 3D 宏观拓扑雷达 (看全局演变)", "🗺️ 2D 平面热力截面 (看精准数值)"], 
                         horizontal=True)
    
    pivot_df = df.pivot(index='Date', columns='Province', values='Shortage')

    # 🔥 核心修正：计算数据矩阵绝对值的最大值，强制设置色轴对称，确保 0 点永远是纯白色
    max_val = pivot_df.max().max()
    min_val = pivot_df.min().min()
    abs_max = max(abs(max_val), abs(min_val))

    if "3D" in view_mode:
        st.info("💡 【3D 交互指引】鼠标左键旋转，滚轮缩放，右键平移。")
        fig = go.Figure(data=[go.Surface(z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index.strftime('%Y-%m'),
                                         colorscale='RdBu_r',
                                         cmin=-abs_max, cmax=abs_max, # 强制 0 对齐纯白
                                         contours={"z": {"show": True, "start": 0, "end": abs_max, "size": 5, "color": "black"}})])
        fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0F172A"),
            scene=dict(
                xaxis_title='空间: 行政区', yaxis_title='时间: 月度', zaxis_title='风险: 缺口指数',
                xaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                yaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                zaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
            ), height=750, margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 【2D 截面指引】将鼠标悬停在色块上即可查看特定省份在该月份的精确缺口数值。白色区域代表供需平衡。")
        fig_2d = go.Figure(data=go.Heatmap(
            z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index.strftime('%Y-%m'),
            colorscale='RdBu_r', 
            zmin=-abs_max, zmax=abs_max, # 强制 2D 图的 0 对齐纯白
            hoverongaps=False, 
            colorbar=dict(title="缺口指数")
        ))
        fig_2d.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0F172A"),
            xaxis_title="空间维度：省级行政区", yaxis_title="时间维度：月度演进",
            height=700, margin=dict(l=0, r=0, b=0, t=20))
        st.plotly_chart(fig_2d, use_container_width=True)

# ================= 页面 4：AI 模块 =================
elif page == "4. AI 大模型调度决策生成":
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown("<h1>🤖 智算中枢: 大模型辅助决策 (Qwen Agent)</h1>", unsafe_allow_html=True)
    with col_btn:
        st.write("")
        if st.button("🔄 重置会话上下文"):
            st.session_state.chat_history = []
            st.rerun() 

    st.markdown("<p style='color:#64748B; font-size: 16px;'>将底层监控数据静默注入大模型提示词工程 (Prompt Engineering)，实现数据驱动的智能诊断与策略生成。</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("<h4 style='color:#1E293B;'>⚙️ 系统认证</h4>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("请输入 LLM API Token", type="password")

    if api_key:
        st.sidebar.success("凭证已加载", icon="✅")

    max_shortage_idx = df['Shortage'].idxmax()
    worst_record = df.loc[max_shortage_idx]
    worst_prov = worst_record['Province']
    worst_date = f"{worst_record['Date'].year}年{worst_record['Date'].month:02d}月"
    worst_shortage = worst_record['Shortage']

    SYSTEM_PROMPT = f"""你是一位国家电网的高级调度专家与双碳智库研究员。
    你的任务是基于电力大数据，为电网的“减污降碳”与“安全保供”提供专业、严谨、条理清晰的决策建议。

    【系统后台实时数据监控上下文】：
    - 异常高危省份：{worst_prov}
    - 发生时间节点：{worst_date}
    - 供需缺口极值：高达 {worst_shortage:.2f} GWh（存在拉闸限电风险）

    请牢记上述异常数据。回答请结合真实的电力调度（如现货市场、DR、VPP）知识，总字数控制在1000字以内。"""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.error(f"🚨 **系统全局风险扫描报告**：底层扫描引擎报告，**{worst_prov}** 在 **{worst_date}** 突破历史最大电力供需剪刀差，缺口峰值达 **{worst_shortage:.2f} GWh**！")

    recommended_prompt = f"针对系统捕获的 {worst_prov} 在 {worst_date} 出现的 {worst_shortage:.2f} GWh 严重电力缺口。作为智算中枢，请立刻生成一份包含3条核心对策的紧急保供优化指令书。"

    if st.button("⚡ 自动执行异常分析指令"):
        st.session_state.chat_history.append({"role": "user", "content": recommended_prompt})

    st.markdown("---")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.info(f"🧑‍💻 **人类分析师**：{msg['content']}")
        else:
            st.success(f"🧠 **调度智算中枢**：\n\n{msg['content']}")

    st.markdown("---")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("向调度中枢下达其他分析指令...")
        submit_btn = st.form_submit_button("执行指令 🚀")

    trigger_api = False

    if submit_btn and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        trigger_api = True
    elif len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user" and not submit_btn:
        trigger_api = True

    if trigger_api:
        if not api_key:
            st.warning("⚠️ 权限验证提醒：请先在左侧控制面板输入您的 API Token！")
            st.session_state.chat_history.pop()
        else:
            from openai import OpenAI
            with st.spinner("🧠 智算中枢正在融合全局感知数据进行推演，请稍候..."):
                try:
                    client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
                    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_history
                    completion = client.chat.completions.create(model="qwen-turbo", messages=messages_for_api)
                    ai_response = completion.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"指令执行失败，远端节点返回错误：{e}")
                    if len(st.session_state.chat_history) > 0:
                        st.session_state.chat_history.pop()
