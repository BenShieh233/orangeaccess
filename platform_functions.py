import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
from options_config import*

# HomeDepot 平台独有的处理函数
def process_homedepot_preview(df):
    st.subheader("HomeDepot 数据预览")
    st.write(df.head())

def process_data(df: pd.DataFrame, 
                 column_to_aggregate: str, 
                 min_rank: int, 
                 max_rank: int, 
                 date_range=None):
    # 确保 date_range 有默认值
    df['Interval'] = pd.to_datetime(df['Interval'])
    df['Interval'] = df['Interval'].dt.date
    if not date_range or len(date_range) != 2:
        date_range = [df['Interval'].min(), df['Interval'].max()]

    # 根据日期范围过滤数据
    filtered_data = df[(df['Interval'] >= date_range[0]) & (df['Interval'] <= date_range[1])]


    # 根据 `column_to_aggregate` 对数据排序
    if column_to_aggregate in ['Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)', 'Click Through Rate (CTR) (sum)']:
        total_summary = filtered_data.groupby(['Campaign ID'])[column_to_aggregate].mean().sort_values(ascending=False)
    else:
        total_summary = filtered_data.groupby(['Campaign ID'])[column_to_aggregate].sum().sort_values(ascending=False)

    # 获取选中的 Campaign ID
    selected_campaigns = total_summary.iloc[min_rank - 1:max_rank].index 
    # 聚合数据，计算每个 'CAMPAIGN ID' 和 'PLACEMENT TYPE' 的值
    aggregated_summary = (
        filtered_data[filtered_data['Campaign ID'].isin(selected_campaigns)]
        .groupby(['Interval', 'Campaign ID', 'Ad Type'])[column_to_aggregate]
        .sum()
        .reset_index()
    )

    return aggregated_summary, total_summary

def plot_homedepot_linechart(df):
    # 初始化 session_state
    if "selected_campaign_id" not in st.session_state:
        st.session_state["selected_param"] = "Spend (sum)"  # 选择一个默认值

    if "aggregation_field" not in st.session_state:
        st.session_state["aggregation_field"] = "Spend (sum)"

    # if "date_range" not in st.session_state:
    #     st.session_state["date_range"] = None

    df = df.dropna(subset=['Ad Type'])
    # 根据选择筛选数据
    df = df[~df['Status'].isin(['system_paused', 'paused'])]
    
    st.subheader("排名比较")
    col1, col2, col3 = st.columns(3)

    with col1:
        # 选择广告状态
        status_options = df['Status'].unique().tolist()
        selected_status = st.multiselect("选择广告状态:", status_options, default=status_options)

    with col2:
        # 选择平台
        platform_options = df['Platform'].unique().tolist()
        selected_platform = st.multiselect("选择平台:", platform_options, default=platform_options)

    with col3:
        # 选择广告类型
        ad_type_options = df['Ad Type'].unique().tolist()
        selected_ad_type = st.multiselect("选择广告类型:", ad_type_options, default=ad_type_options)



    df = df[
        (df['Status'].isin(selected_status)) &
        (df['Platform'].isin(selected_platform)) &
        (df['Ad Type'].isin(selected_ad_type))
    ]

    date_range = st.sidebar.date_input(
        "选择需要分析的时间段:",
        value=[df['Interval'].min(), df['Interval'].max()],
        min_value=df['Interval'].min(),
        max_value=df['Interval'].max(),
    )

    aggregation_field = st.sidebar.selectbox(
        "选择需要分析的参数:", options = HD_metrics
    )

    max_campaigns = len(df['Campaign ID'].unique())
    min_rank, max_rank = st.slider(
        "选择Campaign IDs的排名范围:",
        min_value=1,
        max_value=max_campaigns,
        value=(1, min(5, max_campaigns)),
        step=1
    )
    df['Campaign ID'] = df['Campaign ID'].astype(str)
    aggregated_summary, total_summary = process_data(df,
                                                     aggregation_field,
                                                     min_rank,
                                                     max_rank,
                                                     date_range)    

    fig = px.line(
        aggregated_summary,
        x='Interval',
        y=aggregation_field,
        color='Campaign ID',
        line_dash='Ad Type',
        markers=True,
        title=f"Interactive Trend: {aggregation_field} by Campaign and Placement Type",
        category_orders={'Campaign ID': list(total_summary.index)}
    )

    line_dash_map = {'PLA': 'solid', 'AUCTION_BANNER': 'dash'}
    fig.for_each_trace(lambda trace: trace.update(line=dict(dash=line_dash_map.get(trace.name.split(', ')[1], 'solid'))))

    fig.update_layout(template='plotly_white', hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # 将 total_summary 转换为 DataFrame
    total_summary_df = total_summary.reset_index().rename(columns={'index': 'Campaign ID'})

    # 创建一个映射字典
    id_to_name_mapping = dict(zip(df['Campaign ID'], df['Campaign Name']))

    # 使用 map() 映射 Campaign Name
    total_summary_df['Campaign Name'] = total_summary_df['Campaign ID'].map(id_to_name_mapping)

    plot_bar_chart(total_summary_df, aggregation_field)

    selected_campaign_id = st.sidebar.selectbox("选择需要查看的Campaign ID", options = df['Campaign ID'].unique())
    
    selected_params = st.multiselect("选择需要对比的两个参数", options = HD_metrics, default=['SPA Sales (sum)', 'Spend (sum)'])

    fig_comparison, total_values, ranks = create_comparison_chart(df, selected_campaign_id, selected_params, UNITS_MAPPING)

    st.plotly_chart(fig_comparison)

    # # 显示总值和排名
    # st.write(f"### 周期内总值/平均值和排名")
    # col1, col2 = st.columns(2)
    # col1.metric(
    #     label=f"{selected_params[0]} 平均值/总值 (排名: {ranks[selected_params[0]]})",
    #     value=f"{total_values[selected_params[0]]:.2f} {UNITS_MAPPING.get(selected_params[0], '')}"
    # )
    # col2.metric(
    #     label=f"{selected_params[1]} 平均值/总值 (排名: {ranks[selected_params[1]]})",
    #     value=f"{total_values[selected_params[1]]:.2f} {UNITS_MAPPING.get(selected_params[1], '')}"
    # )    

    display_visual_summary(df, selected_campaign_id, HD_metrics)

def plot_bar_chart(total_summary_df, selected_param):
    """
    使用 Plotly 生成柱状图，从大到小排列 Campaign 的 selected_param 值。
    """
    # 按 selected_param 降序排列
    total_summary_df = total_summary_df.sort_values(by=selected_param, ascending=False)
    total_summary_df["Short Name"] = total_summary_df["Campaign Name"].str.slice(0, 15) + "..."
    total_summary_df['Campaign ID'] = total_summary_df['Campaign ID'].astype(str)
    total_summary_df["Campaign Label"] = total_summary_df["Campaign ID"] + " - " + total_summary_df["Short Name"]

    fig = px.bar(
        total_summary_df,
        x="Campaign Label",  # 用缩短的名称
        y=selected_param,
        text=total_summary_df[selected_param].apply(lambda x: f"${x:,.0f}"),
        color=selected_param,
        color_continuous_scale="Blues"
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        title=f"📊 {selected_param} 排序柱状图",
        xaxis_title="Campaign ID",
        yaxis_title=selected_param,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

def aggregate_params(df: pd.DataFrame, selected_campaign_id: str, selected_params: str):

    # 所有campaign的聚合数据 
    total_summary = df.groupby('Campaign ID')[selected_params].agg(
        {param: ('mean' if param in ['Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)', 'Click Through Rate (CTR) (sum)'] else 'sum') for param in selected_params}
    ).rank(ascending=False, method='min').reset_index()

    campaign_totals = df.groupby('Campaign ID')[selected_params].agg(
        {param: 'mean' if param in ['Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)', 'Click Through Rate (CTR) (sum)'] else 'sum' for param in selected_params}
    ).reset_index()

    # 获取当前 Campaign 的总值或平均值和排名
    total_values = {}
    ranks = {}
    for param in selected_params:
        total_values[param] = campaign_totals.loc[
            campaign_totals['Campaign ID'] == selected_campaign_id, param
        ].values[0]
        ranks[param] = int(total_summary.loc[
            total_summary['Campaign ID'] == selected_campaign_id, param
        ])    

    return total_values, ranks

def display_visual_summary(df: pd.DataFrame, selected_campaign_id: str, selected_params: list):
    """
    以水平条形图的方式展示聚合数据和排名。
    """
    total_values, ranks = aggregate_params(df, selected_campaign_id, selected_params)

    # 创建数据框以供绘图
    data = pd.DataFrame({
        "Parameter": selected_params,
        "Value": [total_values[param] for param in selected_params],
        "Rank": [ranks[param] for param in selected_params]
    })

    # 生成条形图
    fig = px.bar(
        data, 
        x="Value", 
        y="Parameter", 
        text=data["Rank"].apply(lambda r: f"🏆 Rank {r}"), 
        orientation="h", 
        title=f"📊 {selected_campaign_id} 所有指标数据及其排名",
        color="Value",
        color_continuous_scale="Blues"
    )

    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

def create_comparison_chart(df: pd.DataFrame, selected_campaign_id: str, selected_params: list, units_mapping: dict):

    comparison_data = (
        df[df['Campaign ID'] == selected_campaign_id]
        .groupby('Interval')[selected_params]
        .sum()
        .reset_index()
    )

    # 计算总值或平均值及排名
    total_summary = df.groupby('Campaign ID')[selected_params].agg(
        {param: ('mean' if param in ['Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)', 'Click Through Rate (CTR) (sum)'] else 'sum') for param in selected_params}
    ).rank(ascending=False, method='min').reset_index()

    campaign_totals = df.groupby('Campaign ID')[selected_params].agg(
        {param: 'mean' if param in ['Return on Ad Spend (ROAS) SPA (sum)', 'Return on Ad Spend (ROAS) MTA (sum)', 'Click Through Rate (CTR) (sum)'] else 'sum' for param in selected_params}
    ).reset_index()

    # 获取当前 Campaign 的总值或平均值和排名
    total_values = {}
    ranks = {}
    for param in selected_params:
        total_values[param] = campaign_totals.loc[
            campaign_totals['Campaign ID'] == selected_campaign_id, param
        ].values[0]
        ranks[param] = int(total_summary.loc[
            total_summary['Campaign ID'] == selected_campaign_id, param
        ])

    # 映射单位
    units = {param: UNITS_MAPPING.get(param, '') for param in selected_params}

    # 创建双轴折线图
    fig_comparison = go.Figure()

    # 添加第一个参数
    fig_comparison.add_trace(
        go.Scatter(
            x=comparison_data['Interval'],
            y=comparison_data[selected_params[0]],
            mode='lines+markers',
            name=f"{selected_params[0]} (排名: {ranks[selected_params[0]]})",
            yaxis="y1"
        )
    )

    # 添加第二个参数
    fig_comparison.add_trace(
        go.Scatter(
            x=comparison_data['Interval'],
            y=comparison_data[selected_params[1]],
            mode='lines+markers',
            name=f"{selected_params[1]} (排名: {ranks[selected_params[1]]})",
            yaxis="y2"
        )
    )

    # 设置双轴
    fig_comparison.update_layout(
        title=f"Dual-Axis Comparison for Campaign ID: {selected_campaign_id}",
        xaxis=dict(title='Interval'),
        yaxis=dict(title=f"{selected_params[0]} ({units[selected_params[0]]})", side='left'),
        yaxis2=dict(title=f"{selected_params[1]} ({units[selected_params[1]]})", overlaying='y', side='right'),
        template='plotly_white',
        hovermode='x unified'
    )

    return fig_comparison, total_values, ranks




# # # Wayfair 平台独有的处理函数
# # def process_wayfair_preview(df):
# #     st.subheader("Wayfair 数据预览")
# #     st.write(df.head())

# # def process_wayfair_trend(df):
# #     st.subheader("Wayfair 趋势分析")
# #     df['timestamp'] = pd.to_datetime(df['timestamp'])
# #     grouped = df.groupby([df['timestamp'].dt.date, 'campaign_name'])['metric'].sum().reset_index()
# #     fig, ax = plt.subplots()
# #     for campaign in grouped['campaign_name'].unique():
# #         data = grouped[grouped['campaign_name'] == campaign]
# #         ax.plot(data['timestamp'], data['metric'], marker='o', label=campaign)
# #     ax.set_title("Wayfair Campaign Trend")
# #     ax.set_xlabel("Date")
# #     ax.set_ylabel("Metric")
# #     ax.legend()
# #     st.pyplot(fig)

# # # Lowes 平台独有的处理函数
# # def process_lowes_preview(df):
# #     st.subheader("Lowes 数据预览")
# #     st.write(df.head())

# # def process_lowes_trend(df):
# #     st.subheader("Lowes 趋势分析")
# #     df['date'] = pd.to_datetime(df['date'])
# #     grouped = df.groupby([df['date'].dt.date, 'campaign'])['sales'].sum().reset_index()
# #     fig, ax = plt.subplots()
# #     for campaign in grouped['campaign'].unique():
# #         data = grouped[grouped['campaign'] == campaign]
# #         ax.plot(data['date'], data['sales'], marker='o', label=campaign)
# #     ax.set_title("Lowes Campaign Trend")
# #     ax.set_xlabel("Date")
# #     ax.set_ylabel("Sales")
# #     ax.legend()
# #     st.pyplot(fig)

