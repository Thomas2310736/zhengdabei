import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the uploaded Excel file
file_path = r"C:\Users\thoma\Desktop\副本二手数据再处理.xlsx"

# Load the '经济' sheet to examine its contents
df_economy = pd.read_excel(file_path, sheet_name='经济')

# Clean the data and keep only the relevant columns (ID and the economic support values)
df_economy_clean = df_economy[['子女对父母的经济支持（fcamt）']]  # 2020年列

# Rename the columns for clarity
df_economy_clean.columns = ['Economic_Support_2020']

# Filter out rows where there are NaN values in the 'Economic_Support_2020' column
df_economy_clean.dropna(subset=['Economic_Support_2020'], how='any', inplace=True)

# Plot the distribution of economic support in 2020 (using a histogram)
plt.figure(figsize=(10, 6))
plt.hist(df_economy_clean['Economic_Support_2020'], bins=1000, edgecolor='black', color='skyblue')

# Customize the plot
plt.title('Distribution of Economic Support in 2020', fontsize=14)
plt.xlabel('Economic Support Amount (2020)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True)

# Adjust the x-axis range manually (you can change the 0 and 10000 based on your data's range)
plt.xlim(0, 8000)  # Adjust the max value here

# Show the plot
plt.tight_layout()
plt.show()
