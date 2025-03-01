import pandas as pd
import numpy as np
from scipy import stats

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"
df = pd.read_excel(file_path, sheet_name='sheet1', header=1)  # 从第二行开始读取数据

# 特征列（包括你提到的各个维度）
feature_columns = ['有用性1', '易用性1', '风险性1', '社会1', '依赖1', '价值1', '效能1']

# 对每个特征列计算平均值并检验随机性
def runs_test(data):
    n = len(data)
    median = np.median(data)
    data_transformed = [1 if x > median else -1 for x in data]

    # 计算游程数
    runs = np.count_nonzero(np.diff(data_transformed)) + 1  # count the number of changes

    # 计算期望游程数和方差
    expected_runs = (2 * np.sum([x > median for x in data]) * np.sum([x < median for x in data])) / n + 1
    variance_runs = (2 * np.sum([x > median for x in data]) * np.sum([x < median for x in data]) * (2 * np.sum([x > median for x in data]) * np.sum([x < median for x in data]) - n)) / (n ** 2 * (n - 1))

    # 计算Z值
    Z = (runs - expected_runs) / np.sqrt(variance_runs)
    return Z

# 遍历每个特征列，计算平均值并进行随机性检验
for column in feature_columns:
    # 计算特征列的平均值
    column_mean = np.mean(df[column])
    print(f"Mean value of '{column}': {column_mean}")

    # 将特征列的平均值用于游程检验
    Z_value = runs_test([column_mean])
    print(f"Z-value for Runs Test on '{column}': {Z_value}")
    
    # 判断随机性
    alpha = 0.05  # 显著性水平
    if np.abs(Z_value) > stats.norm.ppf(1 - alpha / 2):  # 使用正态分布的临界值
        print(f"数据不符合随机性假设，'{column}' 存在规律性。\n")
    else:
        print(f"数据符合随机性假设，'{column}' 是随机的。\n")
