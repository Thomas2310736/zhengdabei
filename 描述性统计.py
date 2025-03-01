import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 读取Excel文件
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  # 替换为你的文件路径
df = pd.read_excel(file_path,header=1)

# 统计性别比例
gender_counts = df['性别'].value_counts()

# 定义性别标签
labels = ['男', '女']
sizes = [gender_counts.get(1, 0), gender_counts.get(2, 0)]
colors = ['#66b3ff', '#ff9999']  # 蓝色和粉色
explode = (0.1, 0)  # 突出显示男性部分

# 创建饼图
fig, ax = plt.subplots(figsize=(8, 6))

# 绘制饼图
wedges, texts, autotexts = ax.pie(
    sizes, 
    explode=explode, 
    labels=labels, 
    colors=colors, 
    autopct='%1.1f%%', 
    startangle=90, 
    shadow=True,  # 添加阴影
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}  # 添加边框
)

# 设置字体和颜色
plt.setp(autotexts, size=12, weight='bold', color='white')  # 百分比文字颜色
plt.setp(texts, size=14, weight='bold')  # 标签文字样式

# 设置图表标题
ax.set_title('性别比例', fontsize=16, pad=20)

# 显示图表
plt.tight_layout()
plt.show()


