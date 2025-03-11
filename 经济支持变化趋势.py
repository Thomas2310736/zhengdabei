import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 中文显示配置 --------------------------------------------------
# 设置中文字体（根据系统选择可用字体）
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'FangSong']  # 优先使用微软雅黑
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"
df = pd.read_excel(file_path, sheet_name='经济')

# 生成年份序列（假设每个ID连续出现5次代表2011-2020五次调查）
years = [2011, 2013, 2015, 2018, 2020]
df['year'] = df.groupby('ID').cumcount().map(lambda x: years[x] if x < 5 else None)

# 筛选有效数据（每个ID必须有完整的5年数据）
valid_ids = df.groupby('ID').filter(lambda x: (x['year'].count() == 5) & 
                               (x['子女对父母的经济支持（fcamt）'].notnull().all()))['ID'].unique()
clean_df = df[df['ID'].isin(valid_ids)]

# 计算统计量
stat_df = clean_df.groupby('year')['子女对父母的经济支持（fcamt）'].agg(['median', 'mean']).reset_index()

# 可视化设置
plt.figure(figsize=(12, 7))
ax = plt.gca()

# 绘制中位数折线
ax.plot(stat_df['year'], stat_df['median'],
        marker='o', markersize=8, linewidth=2,
        color='#2ca25f', linestyle='--', label='中位数')

# 绘制平均值折线
ax.plot(stat_df['year'], stat_df['mean'],
        marker='s', markersize=8, linewidth=2,
        color='#045a8d', linestyle='-', label='平均值')

# 图表修饰
ax.set_title('子女经济支持年度变化趋势（2011-2020）\n样本量：{}个家庭'.format(len(valid_ids)),
             fontsize=14, pad=15)
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('经济支持金额（元）', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.7)
ax.set_xticks(years)
plt.xticks(rotation=45)

# 添加数据标签
for year, median, mean in zip(stat_df['year'], stat_df['median'], stat_df['mean']):
    ax.text(year, median+50, f'{median:.0f}', 
            ha='center', va='bottom', color='#2ca25f', fontsize=10)
    ax.text(year, mean-80, f'{mean:.0f}', 
            ha='center', va='top', color='#045a8d', fontsize=10)

# 添加图例
ax.legend(loc='upper left', frameon=True, shadow=True)

plt.tight_layout()
plt.show()

# 输出统计结果
print("各年度统计指标：")
print(stat_df.set_index('year'))