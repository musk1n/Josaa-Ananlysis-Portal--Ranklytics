import pandas as pd
import numpy as np
import warnings

# Load the data from the CSV file
file_path = 'combined.csv'
data = pd.read_csv('Ranklytics/home/data/combined.csv')

# Convert relevant columns to numeric
data['Opening Rank'] = pd.to_numeric(data['Opening Rank'], errors='coerce')
data['Closing Rank'] = pd.to_numeric(data['Closing Rank'], errors='coerce')
data['Year'] = pd.to_numeric(data['Year'], errors='coerce')

# Filter data for the past 8 years (2016 to 2023)
data = data[data['Year'].between(2016, 2023)]

# Determine 'Advanced' or 'Mains' based on the Institute name
data['Exam'] = data['Institute'].apply(lambda x: 'Advanced' if pd.notnull(x) and 'Indian Institute  of Technology' in x else ('Advanced' if pd.notnull(x) and 'Indian Institute of Technology' in x else 'Mains'))


# Update 'Gender' based on the year
data.loc[(data['Year'] == 2016) | (data['Year'] == 2017), 'Gender'] = 'Neutral'
data.loc[(data['Year'] != 2016) & (data['Year'] != 2017), 'Gender'] = data['Gender'].apply(lambda x: 'Neutral' if pd.notnull(x) and 'Gender-Neutral' in x else 'Female')



def predict_ranks(data, year):
    predictions = []
    grouped = data.groupby(['Institute', 'Academic Program Name','Quota','Gender', 'Seat Type', 'Exam', 'Round'])

    for name, group in grouped:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=np.RankWarning)

            # Calculate the mean trend of opening and closing ranks
            trend_opening = np.polyfit(group['Year'], group['Opening Rank'], 1)
            trend_closing = np.polyfit(group['Year'], group['Closing Rank'], 1)

        # Predict ranks for the forthcoming year
        predicted_opening = np.polyval(trend_opening, year)
        predicted_closing = np.polyval(trend_closing, year)

        predictions.append({
            'Institute': name[0],
            'Academic Program Name': name[1],
            'Quota': name[2],
            'Gender': name[3],
            'Seat Type': name[4],
            'Exam': name[5],
            'Round': name[6],
            'Predicted Opening Rank': predicted_opening,
            'Predicted Closing Rank': predicted_closing,
            'Year': year
        })

    return pd.DataFrame(predictions)

# Predict ranks for the forthcoming year (2024)
predicted_data = predict_ranks(data, 2024)

# Print the predicted data
predicted_data.to_csv('Predicted_Data', index=False)

file_path = 'Predicted_Data.csv'
df = pd.read_csv(file_path)

# Fill non-finite values with a large number (indicating unavailability)
fill_value = 999999
df['Predicted Opening Rank'] = df['Predicted Opening Rank'].fillna(fill_value).replace([float('inf'), float('-inf')], fill_value)
df['Predicted Closing Rank'] = df['Predicted Closing Rank'].fillna(fill_value).replace([float('inf'), float('-inf')], fill_value)


# Round the predicted opening and closing ranks to the nearest integer
df['Predicted Opening Rank'] = df['Predicted Opening Rank'].round().astype(int)
df['Predicted Closing Rank'] = df['Predicted Closing Rank'].round().astype(int)

# Save the updated dataframe back to a CSV file
updated_file_path = 'Updated_Predicted_Data2.csv'
df.to_csv(updated_file_path, index=False)