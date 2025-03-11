import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 中文显示配置
rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'FangSong']
rcParams['axes.unicode_minus'] = False

# 加载数据
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"
social_df = pd.read_excel(file_path, sheet_name='社交')

# 定义需要处理的社交活动列
activity_cols = [
    '串门、跟朋友交往', '打麻将、下棋、打牌、去社区活动室',
    '向与您不住在一起的亲人、朋友或者邻居提供帮助',
    '跳舞、健身、练气功等', '参加社团组织活动',
    '志愿者活动或者慈善活动', '照顾与您不住在一起的病人或残疾人',
    '上学或者参加培训课程', '炒股', '其他社交活动'
]

# ==== 新增关键步骤：创建social_sum列 ====
social_df[activity_cols] = social_df[activity_cols].fillna(0)
social_df['social_sum'] = social_df[activity_cols].sum(axis=1)  # 计算每个样本的总分

# 生成年份序列
years = [2011, 2013, 2015, 2018, 2020]
social_df['year'] = social_df.groupby('ID').cumcount().map(lambda x: years[x] if x < 5 else None)

# 计算年度平均值
mean_df = social_df.groupby('year')['social_sum'].mean().reset_index()

# 可视化设置
plt.figure(figsize=(10, 5))
ax = plt.gca()

# 绘制趋势线
ax.plot(mean_df['year'], mean_df['social_sum'],
        marker='o', markersize=8, linewidth=2,
        color='#3182bd', linestyle='-')

# 图表修饰
ax.set_title('社交活动参与度年度趋势（2011-2020）', fontsize=14, pad=15)
ax.set_xlabel('年份', fontsize=12)
ax.set_ylabel('平均参与活动数量', fontsize=12)
ax.grid(axis='y', linestyle=':', alpha=0.7)
ax.set_xticks(years)
plt.xticks(rotation=30)
ax.set_ylim(0, mean_df['social_sum'].max()+0.5)  # 自动调整纵轴范围

plt.tight_layout()
plt.show()

# 输出结果
print("各年度平均参与活动数量：")
print(mean_df.set_index('year').round(2))