import pandas as pd
import numpy as np  # 导入 numpy 库
from sklearn.preprocessing import StandardScaler
from semopy import efa

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 处理缺失值和无效值
sheet1_data['多大可能购买'] = sheet1_data['多大可能购买'].fillna(0)
sheet1_data['接触频率'] = sheet1_data['接触频率'].fillna(0) 
sheet1_data = sheet1_data.apply(pd.to_numeric, errors='coerce')
sheet1_data = sheet1_data.fillna(0)

# 替换无穷大和负无穷值
sheet1_data.replace([np.inf, -np.inf], np.nan, inplace=True)
sheet1_data.fillna(0, inplace=True)

# 数据标准化
scaler = StandardScaler()
sheet1_data_standardized = scaler.fit_transform(sheet1_data)
sheet1_data_standardized = pd.DataFrame(sheet1_data_standardized, columns=sheet1_data.columns)

# 使用 EFA 方法探索潜在因子
# 删除了 pval 参数
efa_result = efa.find_latents(sheet1_data_standardized, min_loadings=2, mode='spca', spca_alpha=1.0)

# 打印EFA结果
print("EFA结果：")
print(efa_result)

# 可以选择将模型描述保存到文件
log_file = "efa_output_log.txt"
with open(log_file, "w") as file:
    file.write("探索性因子分析（EFA）结果：\n")
    file.write(str(efa_result) + "\n")

print(f"EFA结果已保存到 {log_file} 文件中")
