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
                    ["1. 源网荷实时态势感知", "2. 电力数据时序分解演进", "3. 省级供需缺口时空图",
                     "4. 智能体调度决策引擎"]
                    )
    st.markdown("---")
    st.success("核心数据库连接正常")
    st.info("系统版本：V 3.3 (Interactive Upgrade)\n\n底层数据：国家统计局、能源局等\n\n智能体：Qwen-Turbo")

# ================= 加载 Excel 数据 =================
@st.cache_data
def load_real_data():
    df = pd.read_excel('power_data.xlsx')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Consumption'] = pd.to_numeric(df['Consumption'], errors='coerce')
    df['Generation'] = pd.to_numeric(df['Generation'], errors='coerce')
    df['Shortage'] = pd.to_numeric(df['Shortage'], errors='coerce')
    return df

df = load_real_data()

# ================= 页面 1：源网荷态势感知大屏 =================
if page == "1. 源网荷实时态势感知":
    st.markdown("<h1>📊 全国省级电网源荷态势感知</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>基于多源传感器及统计局宏观数据，实时监控各省级行政区全社会用电负荷与发电量极值。</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">省级电网监控单元</div><div class="kpi-value">{len(df["Province"].unique())} 个</div><div class="kpi-delta" style="color:#64748B;">覆盖核心电网区域</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card" style="border-top-color: #8B5CF6;"><div class="kpi-title">数据采样时间跨度</div><div class="kpi-value">{len(df["Date"].unique())} 期</div><div class="kpi-delta" style="color:#64748B;">月度高频采样</div></div>', unsafe_allow_html=True)
    with col3:
        max_shortage = df['Shortage'].max()
        st.markdown(f'<div class="kpi-card" style="border-top-color: #EF4444;"><div class="kpi-title">历史最大供需缺口</div><div class="kpi-value">{max_shortage:.1f} <span style="font-size:16px; color:#64748B;">GWh</span></div><div class="kpi-delta delta-up">⚠️ 高压运行警告</div></div>', unsafe_allow_html=True)
    with col4:
        max_gen = df['Generation'].max()
        st.markdown(f'<div class="kpi-card" style="border-top-color: #10B981;"><div class="kpi-title">历史单月最高发电量</div><div class="kpi-value">{max_gen:.1f} <span style="font-size:16px; color:#64748B;">GWh</span></div><div class="kpi-delta delta-down">🟢 产能充沛</div></div>', unsafe_allow_html=True)

    st.write("")
    col_left, col_right = st.columns([1.2, 2])
    with col_left:
        st.markdown("### 📋 省级源荷时序快照 (GWh)")
        formatted_df = df.head(20).copy()
        formatted_df['Date'] = formatted_df['Date'].dt.strftime('%Y-%m')
        st.dataframe(formatted_df.style.format({"Consumption": "{:.1f}", "Generation": "{:.1f}", "Shortage": "{:.1f}"}), hide_index=True, use_container_width=True, height=350)
    with col_right:
        st.markdown("### 📈 选定省份源荷曲线对比")
        sel_prov = st.selectbox("选择目标省份：", df['Province'].unique(), label_visibility="collapsed")
        prov_df = df[df['Province'] == sel_prov]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=prov_df['Date'], y=prov_df['Consumption'], mode='lines', name='全社会用电负荷 (GWh)', line=dict(color='#EF4444', width=3)))
        fig_line.add_trace(go.Scatter(x=prov_df['Date'], y=prov_df['Generation'], mode='lines', name='总发电量 (GWh)', line=dict(color='#10B981', width=3)))
        fig_line.update_layout(template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
            font=dict(color="#334155"), hovermode="x unified", height=350, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor='#E2E8F0', title="时间 (月度)"), yaxis=dict(gridcolor='#E2E8F0', title="电量 (GWh)"))
        st.plotly_chart(fig_line, use_container_width=True)

# ================= 页面 2：电力数据时序分解演进 =================
elif page == "2. 电力数据时序分解演进":
    st.markdown("<h1>📈 电力数据时序乘法分解演进 (Multiplicative Model)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>由于电力规模逐年扩大，系统的波动振幅呈喇叭口发散。我们采用高阶乘法模型 (Y = Trend × Seasonality × Noise) 进行精准降噪分解。</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 交互控件区 ---
    col_ctrl1, col_ctrl2 = st.columns([1, 2])
    with col_ctrl1:
        sel_prov_2 = st.selectbox("🎯 定位分析省份：", df['Province'].unique(), key="prov_2")
    
    prov_df_2 = df[df['Province'] == sel_prov_2].sort_values('Date').copy()
    
    # 获取省份日期范围
    min_date = prov_df_2['Date'].min().date()
    max_date = prov_df_2['Date'].max().date()
    
    with col_ctrl2:
        start_date_2, end_date_2 = st.slider("🗓️ 选择分析时间范围：", 
                                             min_value=min_date, max_value=max_date, 
                                             value=(min_date, max_date), format="YYYY-MM", key="slider_p2")

    # --- 核心数据预处理 (必须在全局计算，防止时间截断导致计算出 NaN) ---
    prov_df_2['Gen_MoM'] = prov_df_2['Generation'].pct_change(periods=1) * 100
    prov_df_2['Gen_YoY'] = prov_df_2['Generation'].pct_change(periods=12) * 100

    ts_series = prov_df_2.set_index('Date')['Generation']
    trend = ts_series.rolling(window=24, center=True, min_periods=6).mean()
    ratio = ts_series / trend
    seasonal_index = ratio.groupby(ratio.index.month).transform('mean')
    seasonality = trend * (seasonal_index - 1)
    noise = ts_series - trend - seasonality
    
    prov_df_2['Trend'] = trend.values
    prov_df_2['Seasonality'] = seasonality.values
    prov_df_2['Noise'] = noise.values

    # --- 执行用户时间切片 ---
    plot_df_2 = prov_df_2[(prov_df_2['Date'].dt.date >= start_date_2) & (prov_df_2['Date'].dt.date <= end_date_2)]

    st.markdown("### 📊 发电量同比/环比及绝对量图")
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(x=plot_df_2['Date'], y=plot_df_2['Generation'], name="月度发电总量 (GWh)", marker_color="#3B82F6", opacity=0.8), secondary_y=False)
    fig2.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Gen_YoY'], name="同比增速 YoY (%)", mode="lines+markers", line=dict(color="#F59E0B", width=3), marker=dict(symbol="diamond", size=6)), secondary_y=True)
    fig2.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Gen_MoM'], name="环比增速 MoM (%)", mode="lines+markers", line=dict(color="#EF4444", width=3, dash="dot"), marker=dict(symbol="circle", size=5)), secondary_y=True)

    fig2.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#334155"),
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), height=450)
    fig2.update_xaxes(gridcolor='#E2E8F0', title="时间 (月度)")
    fig2.update_yaxes(title_text="月度发电总量 (GWh)", secondary_y=False, showgrid=False)
    fig2.update_yaxes(title_text="相对增幅 (%)", secondary_y=True, showgrid=True, gridcolor='#E2E8F0')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.markdown("### 🔬 时序乘法分解：趋势、季节、残差")
    st.markdown("<p style='color:#64748B; font-size: 14px;'>注：长周期趋势扩展为24个月平滑，完美过滤年际干扰；季节性振幅采用动态比率(Ratio)计算，客观反映供需压力的同步放大。</p>", unsafe_allow_html=True)
    
    fig_decomp = make_subplots(rows=4, cols=1, shared_xaxes=True, 
                               subplot_titles=("1. 原始动态增长信号 (GWh)", "2. 跨年度长周期宏观趋势 (GWh)", 
                                               "3. 振幅扩大型季节波动 (GWh)", "4. 突发随机噪声极值点 (GWh)"),
                               vertical_spacing=0.08)

    fig_decomp.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Generation'], line=dict(color="#3B82F6", width=2)), row=1, col=1)
    fig_decomp.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Trend'], line=dict(color="#EF4444", width=3)), row=2, col=1)
    fig_decomp.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Seasonality'], line=dict(color="#10B981", width=2), fill='tozeroy'), row=3, col=1)
    fig_decomp.add_trace(go.Scatter(x=plot_df_2['Date'], y=plot_df_2['Noise'], mode='markers+lines', line=dict(color="#CBD5E1", width=1), marker=dict(color="#475569", size=6, symbol="cross")), row=4, col=1)

    fig_decomp.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                             font=dict(color="#334155"), height=850, showlegend=False, hovermode="x unified")
    fig_decomp.update_xaxes(gridcolor='#E2E8F0')
    fig_decomp.update_yaxes(gridcolor='#E2E8F0')
    st.plotly_chart(fig_decomp, use_container_width=True)

# ================= 页面 3：3D 时空图 =================
elif page == "3. 省级供需缺口时空图":
    st.markdown("<h1>🌐 省级供需缺口时空演化热力曲面</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size: 16px;'>【色彩语义标准】白色基准线为供需平衡点(缺口=0 GWh)。<b style='color:#10B981;'>绿色</b>区域表示电力冗余，<b style='color:#EF4444;'>红色</b>高地代表电网承压严重缺电。</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 顶层交互控件区 ---
    all_provs = df['Province'].unique().tolist()
    col_ctrl1, col_ctrl2 = st.columns([1.5, 1])
    
    with col_ctrl1:
        sel_provs_3 = st.multiselect("🎯 选择对比省份 (支持多选及删除)：", all_provs, default=all_provs)
        if not sel_provs_3:
            st.warning("⚠️ 请至少保留一个对比省份！")
            st.stop()
            
    with col_ctrl2:
        min_date_3 = df['Date'].min().date()
        max_date_3 = df['Date'].max().date()
        start_date_3, end_date_3 = st.slider("🗓️ 选择三维演化时间范围：", 
                                             min_value=min_date_3, max_value=max_date_3, 
                                             value=(min_date_3, max_date_3), format="YYYY-MM", key="slider_p3")

    view_mode = st.radio("👀 请选择观测视角 (View Mode)：", 
                         ["🧊 3D 宏观时空演变地形图", "🗺️ 2D 时空切片热力图"], 
                         horizontal=True)
    
    # 过滤数据
    df_p3 = df[(df['Province'].isin(sel_provs_3)) & 
               (df['Date'].dt.date >= start_date_3) & 
               (df['Date'].dt.date <= end_date_3)]
               
    pivot_df = df_p3.pivot(index='Date', columns='Province', values='Shortage')

    # 核心修正：绝对值对齐
    max_val = pivot_df.max().max()
    min_val = pivot_df.min().min()
    # 防止全是 0 的情况报错
    if pd.isna(max_val): max_val = 1
    if pd.isna(min_val): min_val = -1
    abs_max = max(abs(max_val), abs(min_val))

    # 🔥 核心升级：陡峭型非线性色彩映射，极限压缩白色过渡带
    custom_colorscale = [
        [0.0, '#059669'],   # 深绿 (极端冗余)
        [0.35, '#34D399'],  # 正常绿
        [0.48, '#ECFDF5'],  # 极浅绿 (非常贴近0)
        [0.5, '#FFFFFF'],   # 绝对 0 点 (纯白)
        [0.52, '#FEF2F2'],  # 极浅红 (一过0立刻变红)
        [0.65, '#F87171'],  # 正常红
        [1.0, '#DC2626']    # 深红 (极端短缺)
    ]

    hover_text = []
    for date in pivot_df.index:
        hover_text.append([f"省份: {prov}<br>时间: {date.strftime('%Y年%m月')}<br>缺口数值: {val:.1f} GWh" for prov, val in zip(pivot_df.columns, pivot_df.loc[date])])

    if "3D" in view_mode:
        st.info("💡 【3D 交互指引】鼠标左键旋转，滚轮缩放，右键平移。高地(红色)表征需外部送电支援。")
        fig = go.Figure(data=[go.Surface(z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index.strftime('%Y-%m'),
                                         colorscale=custom_colorscale,
                                         cmin=-abs_max, cmax=abs_max, 
                                         text=hover_text, hoverinfo="text",
                                         colorbar=dict(title="缺口数值 (GWh)"),
                                         contours={"z": {"show": True, "start": 0, "end": abs_max, "size": 5, "color": "black"}})])
        fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0F172A"),
            scene=dict(
                xaxis_title='空间: 行政区', yaxis_title='时间: 月度', zaxis_title='供需缺口 (GWh)',
                xaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                yaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                zaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
                camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
            ), height=750, margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 【2D 切片指引】悬停色块可以查看确切数值。")
        fig_2d = go.Figure(data=go.Heatmap(
            z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index.strftime('%Y-%m'),
            colorscale=custom_colorscale, 
            zmin=-abs_max, zmax=abs_max, 
            text=hover_text, hoverinfo="text",
            colorbar=dict(title="缺口数值 (GWh)")
        ))
        fig_2d.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0F172A"),
            xaxis_title="空间维度：省级行政区", yaxis_title="时间维度：月度演进",
            height=700, margin=dict(l=0, r=0, b=0, t=20))
        st.plotly_chart(fig_2d, use_container_width=True)

# ================= 页面 4：AI 模块 =================
elif page == "4. 智能体调度决策引擎":
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown("<h1>🤖 智能体: 大模型辅助决策 (Qwen‑Turbo)</h1>", unsafe_allow_html=True)
    with col_btn:
        st.write("")
        if st.button("🔄 重置会话上下文"):
            st.session_state.chat_history = []
            st.rerun() 

    st.markdown("<p style='color:#64748B; font-size: 16px;'>将底层监控数据静默注入大模型提示词工程 (Prompt Engineering)，实现数据驱动的智能诊断与策略生成。</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.sidebar.markdown("---")
    st.sidebar.markdown("<h4 style='color:#1E293B;'>⚙️ 系统认证</h4>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("请输入 千问大模型 API Token", type="password")

    if api_key:
        st.sidebar.success("凭证已加载", icon="✅")

    max_shortage_idx = df['Shortage'].idxmax()
    worst_record = df.loc[max_shortage_idx]
    worst_prov = worst_record['Province']
    worst_date = f"{worst_record['Date'].year}年{worst_record['Date'].month:02d}月"
    worst_shortage = worst_record['Shortage']

    SYSTEM_PROMPT = f"""你是一位国家电网高级调度专家 & 双碳智库研究员，掌握电力系统运行、省间现货市场、需求侧响应（DR）、虚拟电厂（VPP）、有序用电等专业知识。

    【实时数据上下文】（仅当用户询问具体数值时使用，若无则忽略）
    - 当前监测到的最严重缺口省份：{worst_prov}（{worst_date} 缺口 {worst_shortage:.2f} GWh，正值表示缺电，负值表示冗余）
    - 其他省份的实时数据未注入，若用户询问，请回答“暂未获取到该省份实时数据，建议查看态势感知大屏”。
    
    【回答规范】
    1. 专业严谨：优先引用国内调度规程（GB/T 31464‑2015《电网运行准则》等）或双碳政策。
    2. 结构清晰：对于策略类问题，用“1. 2. 3.”分点列出；对于概念解释，控制在 200 字以内。
    3. 安全底线：任何建议不得违背“保民生、保安全”原则，禁止推荐非合规市场化手段。
    4. 长度控制：问答决策 ≤1000 字。
    5. 当用户未提供具体数据要求时，允许基于典型电网工况给出通用建议，但需注明“基于典型场景”。
    
    【自由提问处理】
    - 若用户询问数据（如“xx省上月缺口多少？”），请如实告知缺少该数据，并建议用户选择对应省份查看图表。
    - 若用户询问调度策略、双碳路径、技术原理等专业知识，直接依据你的知识库回答，无需依赖上下文数据。 """

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.error(f"🚨 **实时风险扫描简报**：底层扫描引擎报告，**{worst_prov}** 在 **{worst_date}** 突破历史最大电力供需剪刀差，缺口峰值达 **{worst_shortage:.2f} GWh**！")

    recommended_prompt = f"针对系统捕获的 {worst_prov} 在 {worst_date} 出现的 {worst_shortage:.2f} GWh 严重电力缺口。作为智算中枢，请立刻生成一份包含至少3条核心对策的紧急保供调度指令单。"

    if st.button("⚡ 自动执行异常分析指令"):
        st.session_state.chat_history.append({"role": "user", "content": recommended_prompt})

    st.markdown("---")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.info(f"🧑‍💻 **人类分析师**：{msg['content']}")
        else:
            st.success(f"🧠 **调度决策智能体**：\n\n{msg['content']}")

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
            with st.spinner("🧠 智能体正在融合全局感知数据进行推演，请稍候..."):
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
