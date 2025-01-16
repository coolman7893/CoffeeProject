import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Define scoring, with sweeter tastes being lesser score and stronger taste being higher score
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
        print("Usage: python coffee_preferences.py <path_to_csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    # Filtering columns
    relevant_columns = [
        "Before today's tasting, which of the following best described what kind of coffee you like?",
        "How strong do you like your coffee?",
        "What roast level of coffee do you prefer?",
        "What is your age?"
    ]

    filtered_data = data[relevant_columns]
    filtered_data.columns = ["Taste Preference", "Strength Preference", "Roast Preference", "Age Group"]

    # Map each category
    filtered_data["Taste Score"] = filtered_data["Taste Preference"].map(taste_scores)
    filtered_data["Strength Score"] = filtered_data["Strength Preference"].map(strength_scores)
    filtered_data["Roast Score"] = filtered_data["Roast Preference"].map(roast_scores)

    # Calculate the combined score and average 
    filtered_data["Combined Score"] = (
        filtered_data[["Taste Score", "Strength Score", "Roast Score"]].mean(axis=1)
    )

    # Remove rows with missing data
    filtered_data = filtered_data.dropna(subset=["Combined Score", "Age Group"])

    # For Graphing Axis
    age_order = ["<18 years old", "18-24 years old", "25-34 years old", "35-44 years old",
                 "45-54 years old", "55-64 years old", ">65 years old"]
    filtered_data["Age Group"] = pd.Categorical(filtered_data["Age Group"], categories=age_order, ordered=True)

    encoder = OneHotEncoder(sparse_output=False)
    age_encoded = encoder.fit_transform(filtered_data[["Age Group"]])

    # Combine features
    X = np.hstack([filtered_data[["Taste Score", "Strength Score", "Roast Score"]].values, age_encoded])
    y = filtered_data["Combined Score"].values

    # Use MinMaxScaler
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Split into training and validation data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train
    rf = RandomForestRegressor(random_state=42)
    rf.fit(X_train, y_train)

    plt.figure(figsize=(16, 10))
    age_groups = filtered_data["Age Group"].cat.categories
    colors = plt.cm.tab10(np.linspace(0, 1, len(age_groups)))

    # Plot original data and predictions separately f
    for i, age_group in enumerate(age_groups):
        plt.subplot(2, 4, i + 1) 
        group_data = filtered_data[filtered_data["Age Group"] == age_group]

        # Plot actual data
        plt.scatter(
            [age_group] * len(group_data),
            group_data["Combined Score"],
            color=colors[i],
            label="Actual",
            alpha=0.7
        )

        actual_avg = group_data["Combined Score"].mean()
        plt.scatter(
            [age_group], [actual_avg],
            color="blue", marker="*", s=150, label="Actual Avg"
        )
        plt.text(age_group, actual_avg, f"{actual_avg:.2f}", color="blue", fontsize=10)

        # Generate predictions for this age group
        encoded_age_group = encoder.transform([[age_group]])
        random_inputs = np.random.uniform(0, 1, size=(200, X_scaled.shape[1] - encoded_age_group.shape[1]))
        random_inputs = np.hstack([random_inputs, np.tile(encoded_age_group, (200, 1))])
        predicted_scores = rf.predict(random_inputs)

        plt.scatter(
            [f"Predicted {age_group}"] * len(predicted_scores),
            predicted_scores,
            color="red",
            label="Predicted",
            alpha=0.6
        )

        # Compute predicted average
        predicted_avg = np.mean(predicted_scores)
        plt.scatter(
            [f"Predicted {age_group}"], [predicted_avg],
            color="orange", marker="*", s=150, label="Predicted Avg"
        )
        plt.text(f"Predicted {age_group}", predicted_avg, f"{predicted_avg:.2f}", color="orange", fontsize=10)

        plt.title(f"Age Group: {age_group}")
        plt.ylabel("Combined Score")
        plt.xticks(rotation=10)
        plt.legend()

    plt.tight_layout()
    plt.savefig("Coffee_Score_Predicted.png", format="png", dpi=300)
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    print(f"Training Score: {train_score:.4f}")
    print(f"Validation Score: {test_score:.4f}")

if __name__ == "__main__":
    main()