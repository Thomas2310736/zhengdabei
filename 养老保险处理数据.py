import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 中文显示配置
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'FangSong']
rcParams['axes.unicode_minus'] = False

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"
insurance_df = pd.read_excel(file_path, sheet_name='保险')

# 数据预处理
years = [2011, 2013, 2015, 2018]

# 生成年份序列
insurance_df['year'] = insurance_df.groupby('ID').cumcount().map(lambda x: years[x] if x < len(years) else None)

# 清洗数据：分别处理两列
clean_df = insurance_df.dropna(subset=['是否有医疗保险(ins)', '是否有养老保险(pension)']).copy()
clean_df = clean_df[clean_df['year'] != 2020]

# 计算统计量
stat_df = clean_df.groupby('year').agg({
    '是否有医疗保险(ins)': ['median', 'mean'],
    '是否有养老保险(pension)': ['median', 'mean']
}).reset_index()

# 扁平化列名
stat_df.columns = ['year', 
                  'med_ins', 'mean_ins',
                  'med_pension', 'mean_pension']

# 可视化设置
plt.figure(figsize=(12, 7))
ax = plt.gca()

# 使用HSL调色板
colors = {
    '医疗保险': '#1f77b4',  # 蓝色系
    '养老保险': '#ff7f0e'   # 橙色系
}

# 绘制医疗保险趋势
ax.plot(stat_df['year'], stat_df['mean_ins'],
        marker='o', markersize=8, linewidth=2,
        color=colors['医疗保险'], linestyle='-', label='医保-平均值')
"""
ax.plot(stat_df['year'], stat_df['med_ins'],
        marker='o', markersize=8, linewidth=2,
        color=colors['医疗保险'], linestyle='--', label='医保-中位数')
"""
# 绘制养老保险趋势
ax.plot(stat_df['year'], stat_df['mean_pension'],
        marker='s', markersize=8, linewidth=2,
        color=colors['养老保险'], linestyle='-', label='养老-平均值')
"""
ax.plot(stat_df['year'], stat_df['med_pension'],
        marker='s', markersize=8, linewidth=2,
        color=colors['养老保险'], linestyle='--', label='养老-中位数')
"""
# 图表修饰
ax.set_title('社会保障覆盖趋势（2011-2018）\n有效样本量：{}人次'.format(len(clean_df)),
             fontsize=14, pad=15)
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('覆盖率', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.7)
ax.set_xticks(years)
plt.xticks(rotation=45)

# 添加数据标签
for year, m_ins, mn_ins, m_pn, mn_pn in zip(stat_df['year'],
                                           stat_df['med_ins'],
                                           stat_df['mean_ins'],
                                           stat_df['med_pension'],
                                           stat_df['mean_pension']):
    # 医疗保险标签
   

    ax.text(year, mn_ins-0.02, f'{mn_ins:.2f}',
            ha='center', va='top', color=colors['医疗保险'], fontsize=9)

    # 养老保险标签
    
    ax.text(year, mn_pn-0.02, f'{mn_pn:.2f}',
            ha='center', va='top', color=colors['养老保险'], fontsize=9)

# 高级图例设置
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, 
         loc='upper center',
         bbox_to_anchor=(0.5, -0.15),
         ncol=4,
         frameon=True,
         shadow=True,
         fontsize=10)

plt.tight_layout()
plt.show()

# 输出统计结果
print("医疗保险覆盖率统计：")
print(stat_df[['year', 'med_ins', 'mean_ins']].set_index('year').applymap(lambda x: f"{x:.2%}"))

print("\n养老保险覆盖率统计：")
print(stat_df[['year', 'med_pension', 'mean_pension']].set_index('year').applymap(lambda x: f"{x:.2%}"))