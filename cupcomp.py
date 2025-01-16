import pandas as pd
import matplotlib.pyplot as plt
import sys

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
    if len(sys.argv) != 2:
        print("Usage: python coffee_analysis.py <path_to_csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    relevant_columns = [
        "Before today's tasting, which of the following best described what kind of coffee you like?",
        "How strong do you like your coffee?",
        "What roast level of coffee do you prefer?",
        "How many cups of coffee do you typically drink per day?"
    ]

    filtered_data = data[relevant_columns]
    filtered_data.columns = ["Taste Preference", "Strength Preference", "Roast Preference", "Cups Per Day"]

    filtered_data["Taste Score"] = filtered_data["Taste Preference"].map(taste_scores)
    filtered_data["Strength Score"] = filtered_data["Strength Preference"].map(strength_scores)
    filtered_data["Roast Score"] = filtered_data["Roast Preference"].map(roast_scores)

    filtered_data["Combined Score"] = (
        filtered_data[["Taste Score", "Strength Score", "Roast Score"]].mean(axis=1)
    )

    filtered_data["Cups Per Day"] = pd.to_numeric(filtered_data["Cups Per Day"], errors="coerce")
    filtered_data = filtered_data.dropna(subset=["Combined Score", "Cups Per Day"])

    avg_scores_per_cup = filtered_data.groupby("Cups Per Day")["Combined Score"].mean()
    cup_counts = avg_scores_per_cup.index
    scores = avg_scores_per_cup.values

    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_data["Combined Score"], filtered_data["Cups Per Day"], alpha=0.7, label="Data Points")
    plt.scatter(scores, cup_counts, color="red", marker="*", s=150, label="Average per Cup")

    for score, cup_count in zip(scores, cup_counts):
        plt.text(score, cup_count, f"{score:.2f}", fontsize=9, ha='left', va='center')

    plt.title("Coffee Score Vs Daily Cups of Coffee")
    plt.xlabel("Coffee Score")
    plt.ylabel("Cups of Coffee Per Day")
    plt.legend()
    plt.savefig("Cup_Comparison.png", format="png", dpi=300)

if __name__ == "__main__":
    main()