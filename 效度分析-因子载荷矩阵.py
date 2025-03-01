import pandas as pd
import numpy as np
from scipy import stats

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"
df = pd.read_excel(file_path, sheet_name='sheet1', header=1)  # 从第二行开始读取数据

# 定义所有需要的特征维度列
feature_columns = [
    '有用性1', '有用性2', '有用性3', '有用性4',
    '易用性1', '易用性2', '易用性3',
    '风险性1', '风险性2', '风险性3',
    '社会1', '社会2', '社会3', '社会4',
    '依赖1', '依赖2', '依赖3',
    '价值1', '价值2', '价值3',
    '效能1', '效能2', '效能3'
]

# 计算每个维度的平均值
mean_values = df[feature_columns].mean(axis=0)

# 打乱平均值的顺序
shuffled_mean_values = np.random.permutation(mean_values)

# 打印打乱后的平均值
print("Shuffled Mean values for each dimension:")
print(shuffled_mean_values)

# 游程检验函数
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

# 对打乱顺序后的平均值进行游程检验
Z_value = runs_test(shuffled_mean_values)
print(f"\nZ-value for Runs Test on shuffled mean values of dimensions: {Z_value}")

# 判断随机性
alpha = 0.05  # 显著性水平
if np.abs(Z_value) > stats.norm.ppf(1 - alpha / 2):  # 使用正态分布的临界值
    print("数据不符合随机性假设，存在规律性。\n")
else:
    print("数据符合随机性假设。\n")
