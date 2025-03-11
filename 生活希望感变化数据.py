import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 中文显示配置
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'FangSong']
rcParams['axes.unicode_minus'] = False

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"
hope_df = pd.read_excel(file_path, sheet_name='充满希望')

# 数据预处理
years = [2011, 2013, 2015, 2018]  # 删除2020年

# 生成年份序列
hope_df['year'] = hope_df.groupby('ID').cumcount().map(lambda x: years[x] if x < len(years) else None)

# 清洗数据：仅去除目标列的缺失值
clean_df = hope_df.dropna(subset=['对未来充满希望(hope)']).copy()

# 删除2020年的数据
clean_df = clean_df[clean_df['year'] != 2020]

# 计算统计量
stat_df = clean_df.groupby('year')['对未来充满希望(hope)'].agg(['median', 'mean']).reset_index()

# 可视化设置
plt.figure(figsize=(10, 6))
ax = plt.gca()

# 绘制双指标趋势线
ax.plot(stat_df['year'], stat_df['median'],
        marker='o', markersize=8, linewidth=2,
        color='#FF6F61', linestyle='--', label='中位数')  # 珊瑚色

ax.plot(stat_df['year'], stat_df['mean'],
        marker='s', markersize=8, linewidth=2,
        color='#6B5B95', linestyle='-', label='平均值')  # 紫蓝色

# 图表修饰
ax.set_title('生活希望感年度变化趋势（2011-2018）\n有效样本量：{}人次'.format(len(clean_df)),
             fontsize=14, pad=15)
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('希望感评分', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.7)
ax.set_xticks(years)
plt.xticks(rotation=45)

# 添加数据标签，并使标签与数据点保持适当距离
for year, median, mean in zip(stat_df['year'], stat_df['median'], stat_df['mean']):
    ax.text(year, median - 0.05, f'{median:.2f}', 
            ha='center', va='bottom', color='#FF6F61', fontsize=10)
    ax.text(year, mean + 0.05, f'{mean:.2f}', 
            ha='center', va='top', color='#6B5B95', fontsize=10)

# 添加图例
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2),
          ncol=2, frameon=True, shadow=True)

plt.tight_layout()
plt.show()

# 输出统计结果
print("各年度希望感统计：")
print(stat_df.set_index('year').applymap(lambda x: f"{x:.2f}"))
