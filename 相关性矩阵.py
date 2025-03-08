import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体路径（Microsoft YaHei 字体）
font_path = 'C:/Windows/Fonts/msyh.ttc'  # Windows下常见字体路径
font_prop = font_manager.FontProperties(fname=font_path)

# 设置 matplotlib 全局字体为中文
plt.rcParams['font.family'] = font_prop.get_name()  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取数据
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 数据预处理
sheet1_data['多大可能购买'] = sheet1_data['多大可能购买'].fillna(0)
sheet1_data['接触频率'] = sheet1_data['接触频率'].fillna(0)
sheet1_data = sheet1_data.apply(pd.to_numeric, errors='coerce')

# 替换所有的 NaN 为 0
sheet1_data = sheet1_data.fillna(0)

# 替换所有的 Inf 或 -Inf 为 NaN，并用 0 填充
sheet1_data.replace([np.inf, -np.inf], np.nan, inplace=True)
sheet1_data.fillna(0, inplace=True)

# 数据标准化
scaler = StandardScaler()
sheet1_data_standardized = scaler.fit_transform(sheet1_data)

# 将标准化后的数据重新转换为 DataFrame，以便保持列名
sheet1_data_standardized = pd.DataFrame(sheet1_data_standardized, columns=sheet1_data.columns)

# 定义每个观测变量与潜变量之间的因子载荷
factor_loadings_dict = {
    '有用性': [1.0, 1.0438289247658015, 0.8726066449079414, 0.7811031620821428],
    '易用性': [1.0, 1.5845894360676893, 1.4288760147940631],
    '风险性': [1.0, 0.9567622472519449, 0.6705908253736192],
    '社会': [1.0, 0.9545258722608627, 0.7336409242785786, 0.5739896376700762],
    '依赖': [1.0, 0.9440903622791549, 0.7312545455265594],
    '价值': [1.0, 0.893231594035018, 1.0066466217177659],
    '效能': [1.0, 1.1837487563077758, 1.173894436190083]
}

# 定义每个潜变量的观测变量列
latent_vars_to_observed_vars = {
    "有用性": ['有用性1', '有用性2', '有用性3', '有用性4'],
    "易用性": ['易用性1', '易用性2', '易用性3'],
    "风险性": ['风险性1', '风险性2', '风险性3'],
    "社会": ['社会1', '社会2', '社会3', '社会4'],
    "依赖": ['依赖1', '依赖2', '依赖3'],
    "价值": ['价值1', '价值2', '价值3'],
    "效能": ['效能1', '效能2', '效能3']
}

# 为每个潜变量计算得分
latent_scores = pd.DataFrame()

for latent_var, observed_vars in latent_vars_to_observed_vars.items():
    # 获取对应的观测变量的标准化数据
    observed_data = sheet1_data_standardized[observed_vars]
    
    # 获取因子载荷
    factor_loadings = np.array(factor_loadings_dict[latent_var])
    
    # 检查因子载荷的长度是否与观测数据的列数一致
    if len(factor_loadings) != observed_data.shape[1]:
        raise ValueError(f"因子载荷的数量与观测变量的数量不匹配: {latent_var}")
    
    # 计算潜变量得分（加权平均）
    score = np.dot(observed_data, factor_loadings)  # 计算加权得分
    latent_scores[latent_var] = score  # 将得分保存到 DataFrame

# 将“多大可能购买”和“接触频率”加入到潜变量得分中
latent_scores['多大可能购买'] = sheet1_data_standardized['多大可能购买']
latent_scores['接触频率'] = sheet1_data_standardized['接触频率']

# 计算潜变量以及这两个变量之间的相关性矩阵
correlation_matrix = latent_scores.corr()

# 输出相关性矩阵
print("潜变量之间的相关性矩阵：")
print(correlation_matrix)

# 设置 Seaborn 的默认配色方案为 'Blues'
plt.figure(figsize=(10, 8))

# 使用 Seaborn 的 heatmap 创建图表，并明确指定 cmap 参数
sns.heatmap(correlation_matrix, annot=True, center=0, cmap='Blues',  # 使用 'Blues' 配色方案
            linewidths=1, linecolor='black', fmt=".2f", cbar_kws={'shrink': 0.8}, 
            annot_kws={"size": 12, "weight": "bold", "color": "black"})

# 设置背景和边框，模拟阴影效果
plt.gca().set_facecolor('#f7f7f7')  # 设置背景色
plt.gca().patch.set_edgecolor('gray')  # 设置边框颜色
plt.gca().patch.set_linewidth(1)  # 设置边框宽度

# 设置标题，使用中文标题并设置字体
plt.title("潜变量之间的相关性矩阵", fontsize=16, weight='bold', fontproperties=font_prop)

# 设置坐标轴标签
plt.xlabel('潜变量', fontsize=12, weight='bold', fontproperties=font_prop)
plt.ylabel('潜变量', fontsize=12, weight='bold', fontproperties=font_prop)

# 添加坐标轴阴影效果
plt.xticks(rotation=45, ha='right', fontsize=12, weight='bold', fontproperties=font_prop)
plt.yticks(rotation=0, fontsize=12, weight='bold', fontproperties=font_prop)

# 显示图表
plt.show()
