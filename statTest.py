import sys
import pandas as pd
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python coffee_preferences.py <path_to_csv>")
    sys.exit(1)

file_path = sys.argv[1]
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

data = pd.read_csv(file_path)

# This section output p-value and heatmap between age group and coffee preferences

# Drop rows with missing values in these columns
data = data.dropna(subset=["What is your age?", "Before today's tasting, which of the following best described what kind of coffee you like?"])

# Create a contingency table for Chi-Square test
contingency_table = pd.crosstab(data["What is your age?"], data["Before today's tasting, which of the following best described what kind of coffee you like?"])

contingency_table_percentage = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100

# Perform the Chi-Square test
chi2 = chi2_contingency(contingency_table)

print(f"p-value between age group and coffee preferences: {chi2.pvalue}")

alpha = 0.05
if chi2.pvalue < alpha:
    print("Conclusion: There is a significant relationship between age groups and coffee preferences.\n")
else:
    print("Conclusion: No significant relationship between age groups and coffee preferences.\n")

plt.figure(figsize=(10, 6))
sns.heatmap(contingency_table_percentage, annot=True, cmap="YlGnBu", cbar=True)

plt.title("Heatmap of Coffee Preferences by Age Group")
plt.xlabel("Coffee Preferences (in %)")
plt.ylabel("Age Groups")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('coffee_preference_by_age.png', dpi=300)

#plt.show()
################################################################################################################################

# This section output p-value and heatmap between age group and coffee consumption frequency

# Drop rows with missing values in relevant columns
age_consumption_data = data.dropna(subset=["What is your age?", "How many cups of coffee do you typically drink per day?"])

# Create a contingency table
contingency_table = pd.crosstab(age_consumption_data["What is your age?"], age_consumption_data["How many cups of coffee do you typically drink per day?"])

order = ['<18 years old', '18-24 years old', '25-34 years old', '35-44 years old', '45-54 years old', '55-64 years old', '>65 years old']

contingency_table_percentage = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100

contingency_table_percentage = contingency_table_percentage.reindex(order)

# Perform the Chi-Square test
chi2 = chi2_contingency(contingency_table)

print(f"p-value between age group and coffee consumption frequency: {chi2.pvalue}")

alpha = 0.05
if chi2.pvalue < alpha:
    print("Conclusion: There is a significant relationship between age groups and coffee consumption frequency.\n")
else:
    print("Conclusion: No significant relationship between age groups and coffee consumption frequency.\n")
    
contingency_table_percentage.plot(kind='barh', stacked = True, figsize=(20, 12))
plt.title("Stacked Bar Chart of Coffee Consumption Frequency by Age Group")
plt.xlabel("Consumption (in %)")
plt.ylabel("Age Group")
plt.savefig('coffee_consumption_by_age.png', dpi=300)

#plt.show()

################################################################################################################################

#This section prints and output bar chart for most popular and unpopular brewing method for each age group

# Group by age and sum the selections for each brewing method
brewing_columns = [
    "How do you brew coffee at home? (Pour over)",
    "How do you brew coffee at home? (French press)",
    "How do you brew coffee at home? (Espresso)",
    "How do you brew coffee at home? (Coffee brewing machine (e.g. Mr. Coffee))",
    "How do you brew coffee at home? (Pod/capsule machine (e.g. Keurig/Nespresso))",
    "How do you brew coffee at home? (Instant coffee)",
    "How do you brew coffee at home? (Bean-to-cup machine)",
    "How do you brew coffee at home? (Cold brew)",
    "How do you brew coffee at home? (Coffee extract (e.g. Cometeer))",
    "How do you brew coffee at home? (Other)"
]

# Group by age group and sum the brewing method selections
age_group_brewing = data.groupby("What is your age?")[brewing_columns].sum()

most_popular_brewing = age_group_brewing.idxmax(axis=1)
brewing_counts = age_group_brewing.max(axis=1)

least_popular_brewing = age_group_brewing.idxmin(axis=1)
unbrewing_counts = age_group_brewing.min(axis=1)

print("Most Popular Brewing Method for Each Age Group:")
print(most_popular_brewing)

print("Least popular Brewing Method for Each Age Group:")
print(least_popular_brewing)

order = ['<18 years old', '18-24 years old', '25-34 years old', '35-44 years old', '45-54 years old', '55-64 years old', '>65 years old']

# Create a DataFrame to use for plotting
popular_brewing_df = pd.DataFrame({
    'Age Group': most_popular_brewing.index,
    'Most Popular Brewing Method': most_popular_brewing.values,
    'Count': brewing_counts.values
})

popular_brewing_df['Age Group'] = pd.Categorical(popular_brewing_df['Age Group'], categories=order, ordered=True)
popular_brewing_df = popular_brewing_df.sort_values('Age Group')

plt.figure(figsize=(10, 6))
sns.barplot(x='Age Group', y='Count', hue='Most Popular Brewing Method', data=popular_brewing_df)

plt.title("Most Popular Brewing Method by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Frequency of Most Popular Brewing Method")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('most_popular_brewing_by_age.png', dpi=300)

#plt.show()

# Create a DataFrame to use for plotting
unpopular_brewing_df = pd.DataFrame({
    'Age Group': least_popular_brewing.index,
    'Least popular Brewing Method': least_popular_brewing.values,
    'Count': unbrewing_counts.values
})

unpopular_brewing_df['Age Group'] = pd.Categorical(unpopular_brewing_df['Age Group'], categories=order, ordered=True)
unpopular_brewing_df = unpopular_brewing_df.sort_values('Age Group')

plt.figure(figsize=(10, 6))
sns.barplot(x='Age Group', y='Count', hue='Least popular Brewing Method', data=unpopular_brewing_df)

plt.title("Least popular Brewing Method by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Frequency of Least Popular Brewing Method")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('least_popular_brewing_by_age.png', dpi=300)
#plt.show()

################################################################################################################################

# This section output p-value and heatmap between age group and brewing methods

# Define shorter labels for graph label
short_labels = {
    "How do you brew coffee at home? (Pour over)": "Pour Over",
    "How do you brew coffee at home? (French press)": "French Press",
    "How do you brew coffee at home? (Espresso)": "Espresso",
    "How do you brew coffee at home? (Coffee brewing machine (e.g. Mr. Coffee))": "Brewing Machine",
    "How do you brew coffee at home? (Pod/capsule machine (e.g. Keurig/Nespresso))": "Pod Machine",
    "How do you brew coffee at home? (Instant coffee)": "Instant Coffee",
    "How do you brew coffee at home? (Bean-to-cup machine)": "Bean-to-Cup",
    "How do you brew coffee at home? (Cold brew)": "Cold Brew",
    "How do you brew coffee at home? (Coffee extract (e.g. Cometeer))": "Coffee Extract",
    "How do you brew coffee at home? (Other)": "Other"
}

# Drop rows with missing values in relevant columns
brewing_data = data.dropna(subset=["What is your age?"] + brewing_columns)
brewing_data.rename(columns=short_labels, inplace=True)

# Reshape brewing columns
brewing_data_melted = brewing_data.melt(
    id_vars=["What is your age?"],
    value_vars=short_labels.values(),
    var_name="Brewing Method",
    value_name="Count"
)

brewing_data_melted = brewing_data_melted[brewing_data_melted["Count"] > 0]

# Create a contingency table
contingency_table = pd.crosstab(brewing_data_melted["What is your age?"], brewing_data_melted["Brewing Method"])
contingency_table_percentage = contingency_table.div(contingency_table.sum(axis=1), axis=0) * 100

# Perform the Chi-Square test
chi2 = chi2_contingency(contingency_table)

print(f"p-value between age group and brewing method: {chi2.pvalue}")

alpha = 0.05
if chi2.pvalue < alpha:
    print("Conclusion: There is a significant relationship between age groups and brewing methods.\n")
else:
    print("Conclusion: No significant relationship between age groups and brewing methods.\n")

plt.figure(figsize=(12, 8))
sns.heatmap(contingency_table_percentage, annot=True, cmap="YlGnBu", cbar=True)

plt.title("Heatmap of Brewing Methods by Age Group")
plt.xlabel("Brewing Method (in %)")
plt.ylabel("Age Group")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('brewing_method_by_age.png', dpi=300)

# plt.show()
