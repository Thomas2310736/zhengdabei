import pandas as pd
from semopy import Model
import numpy as np
from semopy.stats import calc_chi2, calc_rmsea, calc_cfi, calc_agfi, calc_aic, calc_bic, calc_nfi, calc_tli
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from semopy.report import report
import os

# 读取数据
file_path =r"C:\Users\thoma\Desktop\最新全部数据.xlsx"
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 数据预处理
sheet1_data['多大可能购买'] = sheet1_data['多大可能购买'].fillna(0)
sheet1_data['接触频率'] = sheet1_data['接触频率'].fillna(0) 
sheet1_data = sheet1_data.apply(pd.to_numeric, errors='coerce')
sheet1_data = sheet1_data.fillna(0)
sheet1_data.replace([np.inf, -np.inf], np.nan, inplace=True)
sheet1_data.fillna(0, inplace=True)

# 数据标准化
scaler = StandardScaler()
sheet1_data_standardized = scaler.fit_transform(sheet1_data)
sheet1_data_standardized = pd.DataFrame(sheet1_data_standardized, columns=sheet1_data.columns)

# 结构方程模型描述
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
多大可能购买 ~ 有用性 + 易用性 + 风险性 + 社会 + 依赖 + 价值 + 效能 + 接触频率
接触频率 ~ 有用性 + 易用性 + 风险性 + 社会 + 依赖 + 价值 + 效能

# 潜变量之间的关系
有用性 ~ 易用性 + 价值
风险性 ~ 易用性 + 依赖
社会 ~ 有用性 + 价值
效能 ~ 社会 + 风险性
"""

# 创建模型并进行拟合
model = Model(model_desc)
result = model.fit(sheet1_data_standardized)

# 计算拟合度指标
chi2, p_value = calc_chi2(model)  
rmsea = calc_rmsea(model)
cfi = calc_cfi(model)  
agfi = calc_agfi(model) 
aic = calc_aic(model)
bic = calc_bic(model)
nfi = calc_nfi(model)
tli = calc_tli(model)

# 输出结果到文件
log_file = "model_output_log.txt"
with open(log_file, "w") as file:
    file.write("模型拟合度评估指标：\n")
    file.write(str(result) + "\n\n")  # 输出拟合的结果，包括拟合度指标
    file.write(f"Chi-squared: {chi2}, p-value: {p_value}\n")
    file.write(f"RMSEA: {rmsea}\n")
    file.write(f"CFI: {cfi}\n")
    file.write(f"AGFI: {agfi}\n")
    file.write(f"AIC: {aic}\n")
    file.write(f"BIC: {bic}\n")
    file.write(f"NFI: {nfi}\n")
    file.write(f"TLI: {tli}\n")

    # 获取所有路径系数并输出
    file.write("\n模型的路径系数：\n")
    path_coefficients = model.inspect(mode='list', what='est', information='expected', std_est=False)
    
    for _, row in path_coefficients.iterrows():
        if row['rval'] != row['lval']:  # 排除潜变量与自身的路径
            file.write(f"{row['rval']}（观测变量）与{row['lval']}（潜变量）的路径系数: {row['Estimate']:.3f}\n")

print(f"统计结果已保存到 {log_file} 文件中")

# 获取路径系数矩阵
path_matrix = path_coefficients[['rval', 'lval', 'Estimate']]

# 绘制路径系数热图
plt.figure(figsize=(10, 6))
path_pivot = path_matrix.pivot(index='rval', columns='lval', values='Estimate')
sns.heatmap(path_pivot, annot=True, cmap='coolwarm', cbar=True)
plt.title('路径系数矩阵')
plt.tight_layout()
plt.savefig('path_coefficients.png')
plt.show()

# 绘制拟合度指标的柱状图
fit_indices = {
    'Chi-squared': chi2,
    'RMSEA': rmsea,
    'CFI': cfi,
    'AGFI': agfi,
    'AIC': aic,
    'BIC': bic,
    'NFI': nfi,
    'TLI': tli
}

# 绘制拟合度指标的柱状图
plt.figure(figsize=(10, 6))
sns.barplot(x=list(fit_indices.keys()), y=list(fit_indices.values()))
plt.title('模型拟合度指标')
plt.xlabel('拟合度指标')
plt.ylabel('值')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('fit_indices.png')
plt.show()

# 目标保存路径
output_dir = r"C:\Users\thoma\Desktop\模型报告"  # 设置你想保存报告的文件夹路径

# 确保目标文件夹存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # 如果文件夹不存在，创建它

html_file = os.path.join(output_dir, 'model_report.html')

# 生成报告
report(model, name='模型报告', path=output_dir, std_est=False, se_robust=False)

print(f"HTML 报告已保存为 {html_file}")

