import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据，指定从第二行开始作为标签
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  # 请替换为您的文件路径
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 将“多大可能购买”列转换为数值型，NaN值表示不购买，用0填充
sheet1_data["多大可能购买"] = pd.to_numeric(
    sheet1_data['多大可能购买'], errors='coerce')

# 用0替换NaN值，表示不购买
sheet1_data['多大可能购买'] = sheet1_data['多大可能购买'].fillna(0)

# 将年龄列转换为数值型
sheet1_data['年龄'] = pd.to_numeric(sheet1_data['年龄'], errors='coerce')

# 创建年龄段
bins = [0, 25, 40, 60, float('inf')]
labels = ['25岁以下', '25-40岁', '40-60岁', '60岁以上']
sheet1_data['年龄段'] = pd.cut(sheet1_data['年龄'], bins=bins, labels=labels, right=False)

# 设置Seaborn的样式
sns.set(style="whitegrid")

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 绘制所有年龄段的概率核密度估计（只保留线条，不保留填充区域）
plt.figure(figsize=(10, 6))

for age_group in labels:
    # 获取对应年龄段的数据，并限制数据在0~5之间
    data_for_group = sheet1_data[sheet1_data['年龄段'] == age_group]['多大可能购买']
    data_for_group = data_for_group[(data_for_group >= 0) & (data_for_group <= 5)]  # 过滤0~5范围内的数据
    
    # 使用Seaborn绘制KDE曲线，只保留线条
    sns.kdeplot(data_for_group, label=age_group, fill=False, common_norm=False, linewidth=2)

# 设置x轴显示范围为0~5
plt.xlim(0, 5)

# 添加标题和标签
plt.title('不同年龄段的购买可能性概率密度估计（0~5范围）', fontsize=14)
plt.xlabel('可能购买程度', fontsize=12)
plt.ylabel('密度', fontsize=12)

# 去掉图例
plt.legend().set_visible(False)

# 显示图形
plt.show()

# 计算每个年龄段的购买可能性的平均值
mean_values = sheet1_data.groupby('年龄段')['多大可能购买'].mean()

# 绘制柱状图并加折线
plt.figure(figsize=(10, 6))

# 绘制柱状图
sns.barplot(x=mean_values.index, y=mean_values.values, palette="viridis")

# 添加折线，选择一个更好看的颜色
plt.plot(mean_values.index, mean_values.values, marker='o', color='#1f77b4', label='平均值折线')  # 更漂亮的绿色

# 添加标题和标签
plt.title('不同年龄段的购买可能性平均值', fontsize=14)
plt.xlabel('年龄段', fontsize=12)
plt.ylabel('平均购买可能性', fontsize=12)

# 去掉图例
plt.legend().set_visible(False)

# 显示图形
plt.show()
