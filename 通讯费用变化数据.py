import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 中文显示配置
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'FangSong']
rcParams['axes.unicode_minus'] = False

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"
internet_df = pd.read_excel(file_path, sheet_name='上网')

# 数据预处理
years = [2011, 2013, 2015, 2018, 2020]

# 生成年份序列
internet_df['year'] = internet_df.groupby('ID').cumcount().map(lambda x: years[x] if x < 5 else None)

# 清洗数据：去除负值和缺失值
clean_df = internet_df[
    (internet_df['通讯费用'].notna()) & 
    (internet_df['通讯费用'] >= 0 )
].copy()

# 验证清洗结果
print("数据清洗报告：")
print(f"原始数据量：{len(internet_df)}条")
print(f"清除无效数据：{len(internet_df)-len(clean_df)}条")
print(f"有效数据量：{len(clean_df)}条")

# 计算统计量
stat_df = clean_df.groupby('year')['通讯费用'].agg(['median', 'mean']).reset_index()

# 可视化设置
plt.figure(figsize=(10, 6))
ax = plt.gca()

# 绘制双指标趋势线
ax.plot(stat_df['year'], stat_df['median'],
        marker='o', markersize=8, linewidth=2,
        color='#2ca25f', linestyle='-', label='中位数')  # 绿色线

ax.plot(stat_df['year'], stat_df['mean'],
        marker='s', markersize=8, linewidth=2,
        color='#045a8d', linestyle='-', label='平均值')  # 蓝色线

# 图表修饰
ax.set_title('通讯费用年度变化趋势（2011-2020）\n有效样本量：{}人次'.format(len(clean_df)),
             fontsize=16, pad=15, fontweight='bold', color='#333333')
ax.set_xlabel('年份', fontsize=14, fontweight='bold')
ax.set_ylabel('通讯费用（元）', fontsize=14, fontweight='bold')
ax.grid(axis='y', linestyle=':', alpha=0.7)

# 使年份的x轴标签旋转，避免重叠
ax.set_xticks(years)
plt.xticks(rotation=45, fontsize=12)

# 添加数据标签
for year, median, mean in zip(stat_df['year'], stat_df['median'], stat_df['mean']):
    ax.text(year, median+10, f'{median:.0f}', ha='center', va='bottom', color='#2ca25f', fontsize=12, fontweight='bold')
    ax.text(year, mean-10, f'{mean:.0f}', ha='center', va='top', color='#045a8d', fontsize=12, fontweight='bold')

# 添加图例
ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=12)

# 自动调整布局
plt.tight_layout()
plt.show()

# 输出统计结果
print("\n各年度通讯费用统计（单位：元）：")
print(stat_df.set_index('year').applymap(lambda x: f"{x:.2f}"))
