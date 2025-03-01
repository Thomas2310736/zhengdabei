import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 手动指定字体路径
font_path = 'C:/Windows/Fonts/simhei.ttf'  # SimHei 字体路径
font = FontProperties(fname=font_path, size=14)

# 设置 seaborn 主题和配色
sns.set_theme(style="whitegrid", palette="pastel")

# 读取 Excel 文件
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  # 替换为你的文件路径
df = pd.read_excel(file_path, header=1)

# 假设年龄列的列名是 "年龄"
age_data = df['年龄']

# 创建画布
plt.figure(figsize=(10, 6))

# 绘制直方图 + KDE
sns.histplot(
    age_data, 
    kde=True,  # 开启 KDE
    bins=20,   # 设置直方图的箱子数量
    color='skyblue',  # 直方图颜色
    edgecolor='black',  # 直方图边框颜色
    linewidth=1.2,  # 边框宽度
    alpha=0.7  # 透明度
)

# 设置标题和标签
plt.title('受访者年龄分布 (直方图 + KDE)', fontsize=16, pad=20, fontproperties=font)
plt.xlabel('年龄', fontsize=14, fontproperties=font)
plt.ylabel('频数', fontsize=14, fontproperties=font)

# 显示图表
plt.tight_layout()
plt.show()


# 手动指定字体路径（确保中文显示）
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 替换为你的字体路径
font = FontProperties(fname=font_path, size=14)

# 读取 Excel 文件
file_path = r"C:\Users\thoma\Desktop\773c7ec1023f4de38be8900f0e7ffcb3.xlsx"  # 替换为你的文件路径
df = pd.read_excel(file_path, header=1)

# 假设年龄列的列名是 "年龄"
age_data = df['年龄']

# 统计 50岁以上 和 50岁以下 的人数
below_50 = age_data[age_data < 40].count()  # 50岁以下
above_50 = age_data[age_data >= 40].count()  # 50岁以上

# 创建数据框
age_group = pd.DataFrame({
    '年龄': ['<50', '>50'],
    '人数': [below_50, above_50]
})

# 设置 seaborn 主题和配色
sns.set_theme(style="whitegrid", palette="pastel")

# 创建画布
plt.figure(figsize=(8, 6))

# 绘制条形图
sns.barplot(
    x='年龄', 
    y='人数', 
    data=age_group, 
    palette=['#9467bd', '#8c564b'],  # 自定义颜色
    edgecolor='black',  # 边框颜色
    linewidth=1.2  # 边框宽度
)

# 设置标题和标签
plt.title('50岁以上 vs 50岁以下人数', fontsize=16, pad=20, fontproperties=font)
plt.xlabel('年龄', fontsize=14, fontproperties=font)
plt.ylabel('人数', fontsize=14, fontproperties=font)

# 显示具体数值
for index, value in enumerate(age_group['人数']):
    plt.text(index, value + 0.1, str(value), ha='center', va='bottom', fontsize=12, fontproperties=font)

# 显示图表
plt.tight_layout()
plt.show()