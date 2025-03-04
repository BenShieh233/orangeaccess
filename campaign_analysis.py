import streamlit as st
import pandas as pd
from config import platform_config  # 从配置文件导入
from utils import *

def main():
    # 使用 session_state 保存当前选择的平台
    st.set_page_config(page_title="广告趋势分析", layout="wide")

    if "platform" not in st.session_state:
        st.session_state.platform = None


    # 如果未选择平台，则展示平台选择页面
    if st.session_state.platform is None:
        st.title("请选择数据平台")
        st.write("点击下面按钮进入对应平台的数据处理页面")
        # 动态创建列，平台按钮会根据屏幕宽度自动分列
        num_columns = 3  # 假设你最多有 3 列
        cols = st.columns(num_columns)
        
        # 将平台按钮按列自动排列
        for idx, platform in enumerate(platform_config.keys()):
            col_idx = idx % num_columns  # 确保按钮按列分布
            if cols[col_idx].button(platform):
                st.session_state.platform = platform
                st.rerun()
    else:
        platform = st.session_state.platform
        st.subheader(f"{platform} 平台数据处理",)

        # 侧边栏
        st.sidebar.header("数据处理功能")
        if st.sidebar.button("返回平台选择"):
            st.session_state.platform = None
            st.rerun()

        uploaded_file = st.sidebar.file_uploader("上传Excel文件", type=["xlsx", "xls"])
        if uploaded_file:
            try:
                config = platform_config[platform]
                df = pd.read_excel(uploaded_file, skiprows=config["skiprows"])
                valid, message = validate_file(df, config["required_cols"])

                if valid:
                    st.sidebar.success(message)
                    # 获取当前平台的所有功能
                    func_options = list(config["functions"].keys())
                    selected_func = st.sidebar.selectbox("请选择功能", func_options)

                    # 调用对应功能
                    config["functions"][selected_func](df)
                else:
                    st.sidebar.error(message)
            except Exception as e:
                st.sidebar.error(f"处理文件时发生错误：{e}")
        else:
            st.sidebar.info("请上传Excel文件")


if __name__ == "__main__":
    main()