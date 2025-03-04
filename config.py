from platform_functions import *

platform_config = {
    "HomeDepot": {
        "required_cols": {"Interval", "Status", "Campaign ID","Campaign Name", "Ad Type", "Click Through Rate (CTR) (sum)", "Clicks (sum)"},
        "skiprows": 4,  # 示例：HomeDepot 表格跳过1行
        "functions": {
            "数据预览": process_homedepot_preview,
            "趋势分析": plot_homedepot_linechart,
        }
    },
    # "Wayfair": {
    #     "required_cols": {"campaign_name", "timestamp", "metric"},
    #     "functions": {
    #         "数据预览": process_wayfair_preview,
    #         "趋势分析": process_wayfair_trend
    #     }
    # },
    # "Lowes": {
    #     "required_cols": {"campaign", "date", "sales"},
    #     "functions": {
    #         "数据预览": process_lowes_preview,
    #         "趋势分析": process_lowes_trend
    #     }
    # }
    # 添加新平台时，只需在此增加配置，并在 platform_functions.py 中实现对应函数
}
