import sys
import pandas as pd
import matplotlib.pyplot as plt

# For respondants number
if len(sys.argv) != 2:
    print("Usage: python coffee_preferences.py <path_to_csv>")
    sys.exit(1)

file_path = sys.argv[1]
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    sys.exit(1)

file_path = "GACTT_RESULTS_ANONYMIZED_v2.csv" 
data = pd.read_csv(file_path)

valid_data = data['What is your age?'].dropna()

age_order = ['<18 years old', '18-24 years old', '25-34 years old', 
             '35-44 years old', '45-54 years old', '55-64 years old', '>65 years old']

valid_data = pd.Categorical(valid_data, categories=age_order, ordered=True)

plt.figure(figsize=(10, 6))
plt.hist(valid_data, bins=len(age_order), edgecolor='black', align='mid')
plt.xticks(ticks=range(len(age_order)), labels=age_order, rotation=10)
plt.title('Distribution of Age')
plt.xlabel('Age Group')
plt.ylabel('Frequency')
plt.savefig('age_distribution.png', dpi=300)  # Save as PNG