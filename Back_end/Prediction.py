import pandas as pd
import os
from django.conf import settings
def generate_preference_list(file_path, rank, seat_type, quota, exam, gender,Round_No):
    # Load the CSV file
    try:
        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'Updated_Predicted_Data2.csv')
        df = pd.read_csv(file_path)
        df['Predicted_Opening_Rank'] = pd.to_numeric(df['Predicted_Opening_Rank'], errors='coerce')
        df['Predicted_Closing_Rank'] = pd.to_numeric(df['Predicted_Closing_Rank'], errors='coerce')
        df['Round'] = pd.to_numeric(df['Round'], errors='coerce')
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

    # Ensure column names are correct
    required_columns = ['Seat Type', 'Quota', 'Exam', 'Gender', 'Predicted_Opening_Rank', 'Predicted_Closing_Rank', 'Round', 'Institute', 'Academic_Program_Name']
    for col in required_columns:
        if col not in df.columns:
            print(f"Missing column: {col}")
            return pd.DataFrame()

    # Filter the data based on user criteria
    try:
        filtered_df = df[
            (df['Seat Type'].str.lower() == seat_type.lower()) &
            (df['Quota'].str.lower() == quota.lower()) &
            (df['Exam'].str.lower() == exam.lower()) &
            (df['Gender'].str.lower() == gender.lower()) &
            (((df['Predicted_Opening_Rank'] >= rank)) |
             ((df['Predicted_Opening_Rank'] <= rank) &
              (df['Predicted_Closing_Rank'] >= rank)))&
            (df['Round'] == Round_No)
        ]
    except Exception as e:
        print(f"Error filtering data: {e}")
        return pd.DataFrame()

    # Check if any data remains after filtering
    if filtered_df.empty:
        print("No matching data found for the given criteria.")
        return pd.DataFrame()

    # Sort the data by round and predicted opening rank
    sorted_df = filtered_df.sort_values(by=['Predicted_Opening_Rank'])

    return sorted_df

# Get user input
file_path = 'Updated_Predicted_Data2.csv'
exam = input("Enter the exam type (Advanced/Mains): ")
seat_type = input("Enter your seat type (OPEN/SC/ST/OBC-NCL/OPEN (PwD)/EWS): ")
rank = int(input("Enter your rank: "))
gender = input("Enter your gender (Neutral/Female): ")
if exam != 'Advanced':
    quota = input("Enter the quota (AI/HS/OS): ")
else:
    quota = 'AI'
Round_No = int(input("Round no. :  "))

# Generate and print the preference list
sorted_df = generate_preference_list(file_path, rank, seat_type, quota, exam, gender,Round_No)

if not sorted_df.empty:
    
        round_df = sorted_df
        round_df = round_df.loc[:, ['Institute', 'Academic_Program_Name', 'Predicted_Opening_Rank', 'Predicted_Closing_Rank']]
        print(round_df.to_string(index=False))

else:
    print("No data to display.")
