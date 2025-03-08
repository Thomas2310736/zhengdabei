import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# ======================
# 1. 全局配置
# ======================
# 中文字体配置
try:
    rcParams['font.family'] = 'Microsoft YaHei'  # Windows系统
    # rcParams['font.family'] = 'Songti SC'      # Mac系统
except:
    print("警告：中文字体配置失败，使用默认字体")

rcParams['axes.unicode_minus'] = False  # 显示负号
sns.set_theme(style="whitegrid", palette="pastel")

# ======================
# 2. 数据准备
# ======================
# 读取数据（请确认路径正确！）
try:
    df = pd.read_excel(r"C:\Users\thoma\Desktop\副本问卷数据.xlsx", 
                      sheet_name='sheet1', 
                      header=1)
except Exception as e:
    raise SystemExit(f"文件读取失败: {str(e)}")

# 分类映射字典
EDU_MAP = {
    1: '小学及以下',
    2: '初中',
    3: '普高/中专/技校/职高',
    4: '专科',
    5: '本科',
    6: '硕士及以上'
}

INCOME_MAP = {
    1: '1500元及以下',
    2: '1500-3000元',
    3: '3000-4500元',
    4: '4500-6000元',
    5: '6000元及以上'
}

OCCUPATION_MAP = {  # 新增职业映射
    1: '学生',
    2: '公司职员',
    3: '个体',
    4: '公务员或事业单位工作者',
    5: '退休人员',
    6: '其他'
}

# 数值转分类
df['学历'] = df['学历'].map(EDU_MAP)
df['月收入'] = df['月收入'].map(INCOME_MAP)
df['职业'] = df['职业'].map(OCCUPATION_MAP)  # 新增职业列转换

# ======================
# 3. 数据清洗
# ======================
print("\n数据有效性检查:")
print("学历缺失:", df['学历'].isna().sum())
print("收入缺失:", df['月收入'].isna().sum())
print("职业缺失:", df['职业'].isna().sum())  # 新增职业缺失检查
df = df.dropna(subset=['学历', '月收入', '职业'])  # 新增职业过滤

# ======================
# 4. 生成学历分布图
# ======================
plt.figure(figsize=(10, 6))
edu_counts = df['学历'].value_counts().reindex(EDU_MAP.values(), fill_value=0)
ax = sns.barplot(x=edu_counts.index, y=edu_counts.values, palette="Blues_d")
plt.title('学历分布分析', fontsize=14, pad=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
# 添加数据标签
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')
plt.tight_layout()
plt.savefig(r'C:\Users\thoma\Desktop\学历分布.png', dpi=300, bbox_inches='tight')
plt.close()

# ======================
# 5. 生成月收入分布图
# ======================
plt.figure(figsize=(10, 6))
income_counts = df['月收入'].value_counts().reindex(INCOME_MAP.values(), fill_value=0)
ax = sns.barplot(x=income_counts.index, y=income_counts.values, palette="Greens_d")
plt.title('月收入分布分析', fontsize=14, pad=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
# 添加数据标签
for p in ax.patches:
    ax.annotate(f"{int(p.get_height())}", 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')
plt.tight_layout()
plt.savefig(r'C:\Users\thoma\Desktop\月收入分布.png', dpi=300, bbox_inches='tight')
plt.close()

# ======================
# 6. 生成职业分布图（新增部分）
# ======================
plt.figure(figsize=(12, 6))  # 加宽画布适应较长标签
occupation_counts = df['职业'].value_counts().reindex(OCCUPATION_MAP.values(), fill_value=0)
ax = sns.barplot(x=occupation_counts.index, y=occupation_counts.values, palette="Reds_d")

# 美化设置
plt.title('职业分布分析', fontsize=14, pad=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.xlabel('')
plt.ylabel('人数', fontsize=12)

# 智能调整标签位置
max_count = occupation_counts.max()
yticks = range(0, max_count + 5, 5)  # 自动生成刻度
plt.yticks(yticks)

# 添加数据标签（自动避开0值）
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{int(p.get_height())}", 
                    (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='center', 
                    xytext=(0, 5), 
                    textcoords='offset points')

plt.tight_layout()
plt.savefig(r'C:\Users\thoma\Desktop\职业分布.png', dpi=300, bbox_inches='tight')
plt.close()