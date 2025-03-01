import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据，指定从第二行开始作为标签
file_path = r"C:\Users\thoma\Desktop\副本问卷数据.xlsx"  # 请替换为您的文件路径
sheet1_data = pd.read_excel(file_path, sheet_name='sheet1', header=1)

# 将年龄列转换为数值型
sheet1_data['年龄'] = pd.to_numeric(sheet1_data['年龄'], errors='coerce')

# 将养老方式列（假设列名为 '养老方式'）转换为数值型
sheet1_data['养老方式'] = pd.to_numeric(sheet1_data['养老方式'], errors='coerce')

# 将数据分成两组：年龄大于50和小于等于50
group_older_than_50 = sheet1_data[sheet1_data['年龄'] > 50]
group_50_or_younger = sheet1_data[sheet1_data['年龄'] <= 50]

# 设置Seaborn的样式
sns.set(style="whitegrid")

# 设置中文显示问题
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建一个新的图形窗口
plt.figure(figsize=(12, 6))

# 绘制年龄大于50的养老方式频率分布直方图（逆时针旋转90度，水平柱状图）
plt.subplot(1, 2, 1)
sns.histplot(group_older_than_50['养老方式'], bins=5, kde=False, discrete=True, color='lightcoral', edgecolor='black')
plt.title('年龄大于50的养老方式频率分布')
plt.xlabel('频率')
plt.ylabel('养老方式')
plt.xticks([1, 2, 3, 4, 5], ['家庭养老', '社区养老', '机构养老', '智慧居家养老', '指挥机构养老'])

# 绘制年龄小于等于50的养老方式频率分布直方图（顺时针旋转90度，垂直柱状图）
plt.subplot(1, 2, 2)
sns.histplot(group_50_or_younger['养老方式'], bins=5, kde=False, discrete=True, color='slateblue', edgecolor='black')
plt.title('年龄小于等于50的养老方式频率分布')
plt.xlabel('养老方式')
plt.ylabel('频率')
plt.xticks([1, 2, 3, 4, 5], ['家庭养老', '社区养老', '机构养老', '智慧居家养老', '指挥机构养老'])

# 保证两个柱状图的底部对齐
plt.tight_layout()

# 显示图形
plt.show()
