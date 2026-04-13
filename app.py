import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ================= 页面全局设置 =================
st.set_page_config(page_title="新型电力系统智能调度决策平台", layout="wide", page_icon="⚡",
                   initial_sidebar_state="expanded")

# ================= 自定义 CSS: 极致清晰的现代亮色仪表盘风格 =================
custom_css = """
<style>
    /* 隐藏默认杂项 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 1. 全局背景：极浅的灰蓝色（非刺眼的纯白），让白色卡片能浮现出来 */
    .stApp {
        background-color: #F8FAFC; 
    }

    /* 2. 全局文字：深石板灰，避免纯黑刺眼，护眼且清晰 */
    html, body, [class*="css"], p {
        color: #334155 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* 3. 侧边栏：纯白底色，极其干净 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* 4. 自定义 KPI 卡片：纯白背景 + 悬浮阴影 (高级感来源) */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-top: 4px solid #3B82F6; /* 顶部科技蓝高亮边 */
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .kpi-title {
        color: #64748B; /* 次要文字浅灰 */
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-value {
        color: #0F172A; /* 核心数据极深灰/近黑 */
        font-size: 30px;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-delta {
        font-size: 13px;
        margin-top: 5px;
        font-weight: 600;
    }
    .delta-up { color: #EF4444; } /* 红色高亮 */
    .delta-down { color: #10B981; } /* 绿色高亮 */

    /* 5. 标题层级颜色 */
    h1 { color: #0F172A !important; font-weight: 800 !important; }
    h2, h3, h4, h5 { color: #1E293B !important; font-weight: 700 !important; }

    /* 6. 表格与输入框优化：浅色主题适配 */
    .stDataFrame {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 5px;
    }

    /* 7. 分隔线：极其清淡的灰色 */
    hr {
        border-top: 1px solid #E2E8F0;
        margin: 20px 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ================= 侧边栏导航 =================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #2563EB; font-weight: 900;'>⚡ 智能调度中枢</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #64748B; font-size: 13px; margin-top: -15px;'>Power System Smart Dispatch</p>",
        unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("模块导航",
                    ["1. 源荷态势感知大屏", "2. 新能源时序分解演进", "3. 供需缺口 3D 时空雷达",
                     "4. AI 大模型调度决策生成"]
                    )
    st.markdown("---")
    st.success("核心数据库连接正常")
    st.info("系统版本：V 3.0 (Light UI)\n\n底层数据：国家统计局\n\n智能体：Qwen-Turbo")


# ================= 模拟加载数据 =================
@st.cache_data
def load_dummy_data():
    dates = pd.date_range(start='2018-01-01', end='2023-12-01', freq='MS')
    provinces = ['四川省', '江苏省', '内蒙古自治区', '广东省', '山东省', '浙江省', '新疆维吾尔自治区']
    data = []
    for p in provinces:
        for d in dates:
            month_factor = np.sin(d.month / 12 * 2 * np.pi)
            consumption = 300 + 50 * month_factor + np.random.normal(0, 15)
            generation = 310 + 40 * month_factor + np.random.normal(0, 15)
            data.append([d, p, consumption, generation, consumption - generation])

    df = pd.DataFrame(data, columns=['Date', 'Province', 'Consumption', 'Generation', 'Shortage'])
    return df


df = load_dummy_data()

# ================= 页面 1：源荷大屏 =================
if page == "1. 源荷态势感知大屏":
    st.markdown("<h1>📊 全国省级电网源荷态势感知</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B; font-size: 16px;'>基于多源传感器及统计局宏观数据，实时监控各省级行政区全社会用电负荷与发电量极值。</p>",
        unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">监控省份节点</div>
            <div class="kpi-value">{len(df['Province'].unique())} 个</div>
            <div class="kpi-delta" style="color:#64748B;">覆盖核心电网区域</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #8B5CF6;">
            <div class="kpi-title">数据时序跨度</div>
            <div class="kpi-value">{len(df['Date'].unique())} 期</div>
            <div class="kpi-delta" style="color:#64748B;">月度高频采样</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        max_shortage = df['Shortage'].max()
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #EF4444;">
            <div class="kpi-title">历史最大缺口峰值</div>
            <div class="kpi-value">{max_shortage:.1f} <span style='font-size:16px; color:#64748B;'>GWh</span></div>
            <div class="kpi-delta delta-up">⚠️ 高压运行警告</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        max_gen = df['Generation'].max()
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #10B981;">
            <div class="kpi-title">单月最大发电释放</div>
            <div class="kpi-value">{max_gen:.1f} <span style='font-size:16px; color:#64748B;'>GWh</span></div>
            <div class="kpi-delta delta-down">🟢 产能充沛</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col_left, col_right = st.columns([1.2, 2])
    with col_left:
        st.markdown("### 📋 宏观时序矩阵")
        formatted_df = df.head(20).copy()
        formatted_df['Date'] = formatted_df['Date'].dt.strftime('%Y-%m')
        st.dataframe(formatted_df.style.format({"Consumption": "{:.1f}", "Generation": "{:.1f}", "Shortage": "{:.1f}"}),
                     hide_index=True, use_container_width=True, height=350)
    with col_right:
        st.markdown("### 📈 节点源荷动态追踪")
        sel_prov = st.selectbox("选择目标省份：", df['Province'].unique(), label_visibility="collapsed")
        prov_df = df[df['Province'] == sel_prov]

        fig_line = go.Figure()
        fig_line.add_trace(
            go.Scatter(x=prov_df['Date'], y=prov_df['Consumption'], mode='lines', name='用电负荷 (Consumption)',
                       line=dict(color='#EF4444', width=3)))  # 亮红
        fig_line.add_trace(
            go.Scatter(x=prov_df['Date'], y=prov_df['Generation'], mode='lines', name='发电量 (Generation)',
                       line=dict(color='#10B981', width=3)))  # 亮绿

        # 换为明亮清爽的图表布局
        fig_line.update_layout(
            template="plotly_white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#334155"), hovermode="x unified", height=350, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(gridcolor='#E2E8F0'), yaxis=dict(gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ================= 页面 2：同环比动能剖析 =================
elif page == "2. 新能源时序分解演进":
    st.markdown("<h1>📈 区域电网发电动能剖析 (YoY & MoM)</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B; font-size: 16px;'>应用经典宏观经济学同环比模型，剥离季节性噪音，精准识别产能突变点。</p>",
        unsafe_allow_html=True)
    st.markdown("---")

    sel_prov_2 = st.selectbox("🎯 定位分析省份：", df['Province'].unique(), key="prov_2")
    prov_df_2 = df[df['Province'] == sel_prov_2].sort_values('Date').copy()

    prov_df_2['Gen_MoM'] = prov_df_2['Generation'].pct_change(periods=1) * 100
    prov_df_2['Gen_YoY'] = prov_df_2['Generation'].pct_change(periods=12) * 100

    from plotly.subplots import make_subplots

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    fig2.add_trace(go.Bar(x=prov_df_2['Date'], y=prov_df_2['Generation'],
                          name="月度发电总量 (GWh)", marker_color="#3B82F6", opacity=0.8),  # 科技蓝
                   secondary_y=False)
    fig2.add_trace(go.Scatter(x=prov_df_2['Date'], y=prov_df_2['Gen_YoY'],
                              name="同比增速 YoY (%)", mode="lines+markers",
                              line=dict(color="#e6d115", width=3), marker=dict(symbol="diamond", size=6)),  # 亮橙
                   secondary_y=True)
    fig2.add_trace(go.Scatter(x=prov_df_2['Date'], y=prov_df_2['Gen_MoM'],
                              name="环比增速 MoM (%)", mode="lines+markers",
                              line=dict(color="#fa0511", width=3), marker=dict(symbol="circle", size=5)),
                   # 亮绿
                   secondary_y=True)

    fig2.update_layout(
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#334155"),
        title_text=f"<b>{sel_prov_2} 核心发电指标演化矩阵</b>", title_font_size=18,
        hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=550
    )
    fig2.update_xaxes(gridcolor='#E2E8F0')
    fig2.update_yaxes(title_text="绝对产出 (GWh)", secondary_y=False, showgrid=False)
    fig2.update_yaxes(title_text="相对增幅 (%)", secondary_y=True, showgrid=True, gridcolor='#E2E8F0')

    st.plotly_chart(fig2, use_container_width=True)

# ================= 页面 3：3D 时空图 =================
elif page == "3. 供需缺口 3D 时空雷达":
    st.markdown("<h1>🌐 区域互济缺口 3D 时空推演雷达</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#64748B; font-size: 16px;'>【交互指引】使用鼠标左键旋转拓扑结构，滚轮缩放，右键平移。高地(红色)表征电网处于深度承压状态。</p>",
        unsafe_allow_html=True)
    st.markdown("---")

    pivot_df = df.pivot(index='Date', columns='Province', values='Shortage')

    # 【完美还原】采用你指定的极具专业感和视觉冲击力的 红-白-蓝 渐变色
    fig = go.Figure(data=[go.Surface(z=pivot_df.values, x=pivot_df.columns, y=pivot_df.index.strftime('%Y-%m'),
                                     colorscale='RdBu_r',  # 红蓝配色 (Red-Blue reverse)
                                     contours={"z": {"show": True, "start": 0, "end": max(pivot_df.max()), "size": 10,
                                                     "color": "black"}})])

    fig.update_layout(
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#0F172A"),
        scene=dict(
            xaxis_title='空间维度: 行政区',
            yaxis_title='时间维度: 月度',
            zaxis_title='风险维度: 缺口指数',
            xaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
            yaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
            zaxis=dict(gridcolor="#CBD5E1", backgroundcolor="#F8FAFC", showbackground=True),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
        ),
        height=750, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig, use_container_width=True)

# ================= 页面 4：AI 模块 =================
elif page == "4. AI 大模型调度决策生成":
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown("<h1>🤖 智算中枢: 大模型辅助决策 (Qwen Agent)</h1>", unsafe_allow_html=True)
    with col_btn:
        st.write("")
        if st.button("🔄 重置会话上下文", help="清空记忆，开启新的研判任务"):
            st.session_state.chat_history = []
            st.experimental_rerun()

    st.markdown(
        "<p style='color:#64748B; font-size: 16px;'>将底层监控数据静默注入大模型提示词工程 (Prompt Engineering)，实现数据驱动的智能诊断与策略生成。</p>",
        unsafe_allow_html=True)
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
    你的任务是基于电力大数据（源荷态势、新能源消纳等），为电网的“减污降碳”与“安全保供”提供专业、严谨、条理清晰的决策建议。

    【系统后台实时数据监控上下文】：
    当前系统通过跨表扫描发现核心异常极值：
    - 异常高危省份：{worst_prov}
    - 发生时间节点：{worst_date}
    - 供需缺口极值：高达 {worst_shortage:.2f} GWh（用电量远超发电量，存在拉闸限电风险）

    请你牢记上述异常数据。回答请尽可能结合真实的电力调度（如现货市场、DR、VPP）及严谨的电网运行知识，总字数控制在1000字以内。"""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.error(
        f"🚨 **系统监控中断预警**：底层扫描引擎报告，**{worst_prov}** 在 **{worst_date}** 突破历史最大电力供需剪刀差，缺口峰值达 **{worst_shortage:.2f} GWh**！")

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
    elif len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1][
        "role"] == "user" and not submit_btn:
        trigger_api = True

    if trigger_api:
        if not api_key:
            st.warning("⚠️ 权限验证提醒：请先在左侧控制面板输入您的 API Token！")
            st.session_state.chat_history.pop()
        else:
            from openai import OpenAI

            with st.spinner("🧠 智算中枢正在融合全局感知数据进行推演，请稍候..."):
                try:
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                    )

                    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_history

                    completion = client.chat.completions.create(
                        model="qwen-turbo",
                        messages=messages_for_api
                    )

                    ai_response = completion.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    st.experimental_rerun()

                except Exception as e:
                    st.error(f"指令执行失败，远端节点返回错误：{e}")
                    if len(st.session_state.chat_history) > 0:
                        st.session_state.chat_history.pop()