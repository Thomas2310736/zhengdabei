import pandas as pd
from factor_analyzer import FactorAnalyzer
import numpy as np

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name='sheet1', header=1)

# 设置需要进行因子分析的列，这些列应该是你的维度问题项（如有用性、易用性等）
# 这里我们将所有维度的题目都包含进去
efa_columns = [
    '有用性1', '有用性2', '有用性3', '有用性4',
    '易用性1', '易用性2', '易用性3',
    '风险性1', '风险性2', '风险性3',
    '社会1', '社会2', '社会3', '社会4',
    '依赖1', '依赖2', '依赖3',
    '价值1', '价值2', '价值3',
    '效能1', '效能2', '效能3'
]

# 提取所需列的数据
efa_data = df[efa_columns].dropna()  # 删除包含NaN的行

# 标准化数据（因子分析前通常需要标准化数据）
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
efa_data_scaled = scaler.fit_transform(efa_data)

# 进行因子分析
fa = FactorAnalyzer(n_factors=7, rotation='varimax')  # 7个因子，使用正交旋转（varimax）
fa.fit(efa_data_scaled)

# 输出因子负荷矩阵，查看每个问题的因子载荷
factor_loadings = fa.loadings_

# 打印因子负荷矩阵
print("因子负荷矩阵：")
print(factor_loadings)

# 查看每个因子的方差解释（解释的方差比例）
explained_variance = fa.get_factor_variance()
print("\n每个因子的方差解释：")
print(explained_variance)

# 计算KMO检验值，检查数据是否适合做因子分析
from factor_analyzer import calculate_kmo
kmo_all, kmo_model = calculate_kmo(efa_data_scaled)
print(f"\nKMO检验值: {kmo_model}")
