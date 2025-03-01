import pandas as pd
from scipy.stats import pearsonr
import numpy as np

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='sheet1',header=1)  # 选择需要的工作表
dimension_columns = {
    '有用性': ['有用性1', '有用性2', '有用性3', '有用性4'],  # 示例，有4个问题
    '易用性': ['易用性1', '易用性2', '易用性3'],              # 示例，3个问题
    '风险性': ['风险性1', '风险性2','风险性3'],                           # 示例，2个问题
    '社会': ['社会1', '社会2', '社会3','社会4'],              # 示例，4个问题
    '依赖': ['依赖1', '依赖2', '依赖3'],                        # 示例，3个问题
    '价值': ['价值1', '价值2', '价值3'],              # 示例，4个问题
    '效能': ['效能1', '效能2','效能3']                                   # 示例，2个问题
}

# 提取每个维度的列数据并计算Cronbach's alpha
def cronbach_alpha(data):
    item_variances = data.var(ddof=1, axis=0)  # 每个问题的方差
    total_variance = data.sum(axis=1).var(ddof=1)  # 所有问题的总方差
    k = data.shape[1]  # 问题数量
    return (k / (k - 1)) * (1 - item_variances.sum() / total_variance)

# 存储每个维度的Cronbach's alpha值
alpha_values = {}

for dim, cols in dimension_columns.items():
    # 获取当前维度的所有问题列
    dimension_data = df[cols].dropna()  # 删除包含NaN的行
    alpha = cronbach_alpha(dimension_data)
    alpha_values[dim] = alpha

# 打印每个维度的Cronbach's alpha值
print("各维度的Cronbach's alpha值:")
for dim, alpha in alpha_values.items():
    print(f"{dim}: {alpha:.4f}")