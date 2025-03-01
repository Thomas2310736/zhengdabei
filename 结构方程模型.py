import pandas as pd
from semopy import Model

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  # 请修改为您的文件路径
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 清理数据（将空值替换为0，并确保数据是数值型）
sheet1_data['多大可能购买'] = sheet1_data['多大可能购买'].fillna(0)
sheet1_data = sheet1_data.apply(pd.to_numeric, errors='coerce')

# 定义模型（测量模型和结构模型）
model_desc = """
# 测量模型（定义潜变量和其观测变量的关系）
有用性 =~ 有用性1 + 有用性2 + 有用性3 + 有用性4
易用性 =~ 易用性1 + 易用性2 + 易用性3
风险性 =~ 风险性1 + 风险性2 + 风险性3
社会 =~ 社会1 + 社会2 + 社会3 + 社会4
依赖 =~ 依赖1 + 依赖2 + 依赖3
价值 =~ 价值1 + 价值2 + 价值3
效能 =~ 效能1 + 效能2 + 效能3

# 结构模型（潜变量之间的关系）
多大可能购买 ~ 有用性 + 易用性 + 风险性 + 社会 + 依赖 + 价值 + 效能
易用性 ~ 有用性
社会 ~ 风险性
"""

# 构建并拟合模型
model = Model(model_desc)
model.fit(sheet1_data)

# 获取模型的拟合度指标
fit_indices = model.fit()  # 这里我们直接拟合并获取模型拟合信息
print("模型拟合度评估指标：")
print(fit_indices)

# 获取因子载荷
loadings = model.inspect()
print("\n每个维度下的因子载荷：")
print(loadings)
