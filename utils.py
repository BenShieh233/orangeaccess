# 通用的文件校验函数：检查 DataFrame 是否包含必需的列
def validate_file(df, required_cols):
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        return False, f"文件格式错误：缺少必要的列 {', '.join(missing)}"
    return True, "文件格式正确"