import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import seaborn as sns
import pandas as pd
import textwrap

# Load your data
data = pd.read_csv('data/summary.csv')  # Replace with the correct path to your CSV file

price_data = data[['region_name', 'category', 'mean price [€]']]

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating the bar plot

import matplotlib.pyplot as plt
# Load your data
data = pd.read_csv('data/summary.csv')  # Replace with the correct path to your CSV file

# Calculate the mean of the mean price for each category
mean_price_category = price_data.groupby('category')['mean price [€]'].mean().sort_values()

sorted_categories = mean_price_category.index.tolist()

price_data = data[['region_name', 'category', 'mean price [€]']]

# Setting the aesthetic style of the plots
sns.set_style("whitegrid")

# Creating the bar plot
plt.figure(figsize=(15, 8))
ax = sns.barplot(x='mean price [€]', y='category', hue='region_name', data=price_data, order=sorted_categories, errorbar=None)

# Wrap long category names into multiple lines
ax.set_yticklabels([textwrap.fill(label.get_text(), 20) for label in ax.get_yticklabels()])
plt.title('Mean Price Comparison Across Regions for Each Category')
plt.xlabel('Mean Price (€)')
plt.ylabel('Category')
plt.legend(title='Region')
plt.subplots_adjust(left=0.15)  # Adjust the plot's size to make room for the legend
plt.show()