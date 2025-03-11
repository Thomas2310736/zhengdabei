import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.font_manager as fm
import warnings

# ======================
# 1. 全局配置
# ======================
# 过滤警告
warnings.filterwarnings("ignore")

# 手动加载中文字体（确保路径正确）
font_path = r'C:\Windows\Fonts\msyh.ttc'  # Windows微软雅黑
# font_path = '/System/Library/Fonts/STHeiti Medium.ttc'  # Mac系统字体

try:
    # 注册字体
    font_prop = fm.FontProperties(fname=font_path)
    rcParams['font.family'] = font_prop.get_name()
    rcParams['axes.unicode_minus'] = False  # 显示负号
    
    # 验证字体是否生效
    if not fm.findfont(font_prop):
        raise ValueError("字体注册失败")
except Exception as e:
    print(f"字体加载失败: {str(e)}")
    print("请检查字体路径或手动安装中文字体")

# ======================
# 2. 数据准备
# ======================
# （数据加载和清洗部分保持不变）
try:
    df = pd.read_excel(r"C:\Users\thoma\Desktop\副本问卷数据.xlsx", 
                      sheet_name='sheet1', 
                      header=1)
except Exception as e:
    raise SystemExit(f"文件读取失败: {str(e)}")

# 分类映射字典（保持不变）
EDU_MAP = {1: '小学及以下', 2: '初中', 3: '普高/中专/技校/职高', 
          4: '专科', 5: '本科', 6: '硕士及以上'}
INCOME_MAP = {1: '1500元及以下', 2: '1500-3000元', 3: '3000-4500元',
             4: '4500-6000元', 5: '6000元及以上'}
OCCUPATION_MAP = {1: '学生', 2: '公司职员', 3: '个体',
                4: '公务员或事业单位工作者', 5: '退休人员', 6: '其他'}

# 数值转分类
df['学历'] = df['学历'].map(EDU_MAP)
df['月收入'] = df['月收入'].map(INCOME_MAP)
df['职业'] = df['职业'].map(OCCUPATION_MAP)

# 数据清洗
df = df.dropna(subset=['学历', '月收入', '职业'])

# ======================
# 3. 独立可视化函数（优化版）
# ======================
def create_single_plot(data, title, palette, filename):
    """生成单张独立图表"""
    plt.figure(figsize=(10, 6), dpi=120)  # 独立画布
    
    # 生成排序数据
    ordered_data = data.value_counts().reindex(data.cat.categories, fill_value=0)
    
    # 创建条形图
    ax = sns.barplot(
        x=ordered_data.index,
        y=ordered_data.values,
        palette=palette,
        saturation=0.8,
        edgecolor='black',
        linewidth=1
    )
    
    # 标题和标签
    plt.title(title, fontsize=14, pad=15, fontweight='bold', 
             fontproperties=font_prop)
    plt.xticks(rotation=45, ha='right', fontproperties=font_prop)
    plt.ylabel('人数', fontproperties=font_prop)
    
    # 添加数据标签
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.0f}",
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='center',
            xytext=(0, 5),
            textcoords='offset points',
            fontsize=10,
            fontproperties=font_prop
        )
    
    # 保存和清理
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已保存: {filename}")

# ======================
# 4. 生成独立图表
# ======================
if __name__ == "__main__":
    # 设置分类顺序
    df['学历'] = pd.Categorical(df['学历'], categories=EDU_MAP.values())
    df['月收入'] = pd.Categorical(df['月收入'], categories=INCOME_MAP.values())
    df['职业'] = pd.Categorical(df['职业'], categories=OCCUPATION_MAP.values())
    
    # 生成学历分布图（蓝色系）
    create_single_plot(
        df['学历'],
        "消费者学历分布分析",
        "Blues_d",
        r"C:\Users\thoma\Desktop\学历分布.png"
    )
    
    # 生成月收入分布图（绿色系）
    create_single_plot(
        df['月收入'],
        "消费者月收入分布分析",
        "Greens_d",
        r"C:\Users\thoma\Desktop\月收入分布.png"
    )
    
    # 生成职业分布图（红色系）
    create_single_plot(
        df['职业'],
        "消费者职业分布分析",
        "Reds_d",
        r"C:\Users\thoma\Desktop\职业分布.png"
    )