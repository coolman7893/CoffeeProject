import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Define scoring dictionaries for preferences
taste_scores = {
    "Fruity": 3, "Chocolatey": 5, "Full-Bodied": 7, "Bright": 4, "Nutty": 6,
    "Sweet": 2, "Caramalized": 5, "Juicy": 4, "Bold": 8, "Floral": 3, "Complex": 6, "Light": 1
}

strength_scores = {
    "Light": 1, "Medium": 3, "Dark": 5, "Nordic": 2, "Blonde": 2, "Italian": 4, "French": 5
}

roast_scores = {
    "Somewhat strong": 3, "Medium": 5, "Very strong": 7, "Somewhat light": 2, "Weak": 1
}

def main():
    # Ensure the file path is provided
    if len(sys.argv) != 2:
        print("Usage: python coffee_preferences.py <path_to_csv>")
        sys.exit(1)

    # Load the CSV file
    file_path = sys.argv[1]
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    # Filtering relevant columns
    relevant_columns = [
        "Before today's tasting, which of the following best described what kind of coffee you like?",
        "How strong do you like your coffee?",
        "What roast level of coffee do you prefer?",
        "What is your age?"
    ]

    filtered_data = data[relevant_columns]
    filtered_data.columns = ["Taste Preference", "Strength Preference", "Roast Preference", "Age Group"]

    # Map scores to each category
    filtered_data["Taste Score"] = filtered_data["Taste Preference"].map(taste_scores)
    filtered_data["Strength Score"] = filtered_data["Strength Preference"].map(strength_scores)
    filtered_data["Roast Score"] = filtered_data["Roast Preference"].map(roast_scores)

    # Calculate the combined score and average it
    filtered_data["Combined Score"] = (
        filtered_data[["Taste Score", "Strength Score", "Roast Score"]].mean(axis=1)
    )

    # Remove rows with missing data for the analysis
    filtered_data = filtered_data.dropna(subset=["Combined Score", "Age Group"])

    # Reorder age groups
    age_order = ["<18 years old", "18-24 years old", "25-34 years old", "35-44 years old",
                 "45-54 years old", "55-64 years old", ">65 years old"]
    filtered_data["Age Group"] = pd.Categorical(filtered_data["Age Group"], categories=age_order, ordered=True)

    # Plotting the scatterplot
    plt.figure(figsize=(12, 6))
    age_groups = filtered_data["Age Group"].cat.categories
    colors = plt.cm.tab10(np.linspace(0, 1, len(age_groups)))

    scatter_points = []  # To store legend entries
    for i, age_group in enumerate(age_groups):
        group_data = filtered_data[filtered_data["Age Group"] == age_group]
        scatter = plt.scatter(
            [age_group] * len(group_data),
            group_data["Combined Score"],
            color=colors[i],
            label=age_group,
            alpha=0.7
        )
        scatter_points.append(scatter)
        
        # Highlight the average highest score for this age group
        max_average_score = group_data["Combined Score"].mean()
        avg_high_marker = plt.scatter(
            [age_group], [max_average_score], 
            color="black", marker="*", s=150
        )

    # Add a manual legend to ensure Avg High is at the top
    legend_entries = [avg_high_marker] + scatter_points
    legend_labels = ["Avg High"] + list(age_groups)

    plt.title("Coffee Taste Preferences by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Taste Score (Averaged)")
    plt.legend(legend_entries, legend_labels, title="Age Group", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("Coffee_Score", format='png', dpi=300)
    
    

if __name__ == "__main__":
    main()
