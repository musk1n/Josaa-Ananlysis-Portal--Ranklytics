# ##1 branch and college according to Rank
# import pandas as pd
# import numpy as np
# import os
# from django.conf import settings

# def get_choices_by_rank(adv_rank, mains_rank, seatty, gender, state, year):
#     # Construct the full path to the CSV file
#     file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
#     file = pd.read_csv(file_path)
#     file_path2 = os.path.join(settings.BASE_DIR, 'home', 'data', 'Seat_State_Matrix.csv')
#     seats_file = pd.read_csv(file_path2)
#     seats_file.dropna(subset='Total (includes Female Supernumerary)', inplace=True)

#     # Filter IIT and non-IIT data for round 6 and year 2023
#     file1 = file.loc[
#         (file['Round'] == 6) & 
#         (file['Year'] == year) & 
#         ((file['Institute'].str.contains('Indian Institute  of Technology', case=False, na=False)) |
#          (file['Institute'].str.contains('Indian Institute of Technology', case=False, na=False)))
#     ]

#     file2 = file.loc[
#         (file['Round'] == 6) & 
#         (file['Year'] == year) & 
#         (~(file['Institute'].str.contains('Indian Institute  of Technology', case=False, na=False)))
#     ]

#     # Get user inputs
#     #adv_rank = int(input("Enter Your Advanced Rank:"))
#     #mains_rank = int(input("Enter Your Mains Rank:"))
#     #seatty = input("Enter Your seat type(OPEN,EWS,OBC-NCL,SC,ST,EWS (PwD),OBC-NCL (PwD),OPEN (PwD), SC (PwD), ST(PwD)):")
#     #gender = input("Enter Your Gender(Male,Female):")
#     #state = input("Enter Your State:")
#     state = state.upper()

#     # Filter state quota from seats_file
#     state_quota = seats_file.loc[seats_file['State/All India Seats'] == state]
#     home_state_institute = state_quota['Institute Name']

#     # Define gender list based on input
#     gender_list = ['Female-only (including Supernumerary)'] if gender.lower() == 'female' else ['Gender-Neutral']

#     # Convert ranks to numeric, coercing errors to NaN, and drop rows with NaN values in relevant columns
#     for df in [file1, file2]:
#         df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce').astype('Int64')
#         df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
#         df.dropna(subset=['Closing Rank', 'Institute'], inplace=True)
#         df['Closing Rank']=df['Closing Rank'].astype('Int64')

#     # Filter choices for IITs
#     choices_iit = file1.loc[
#         (((adv_rank >= file1['Opening Rank']) & 
#           (adv_rank <= file1['Closing Rank']))|
#          (adv_rank <= file1['Opening Rank'])) & 
#         (seatty.upper() == file1['Seat Type']) & 
#         (file1['Gender'].isin(gender_list))
#     ]

#     # Filter choices for other institutes
#     choices_other = file2.loc[
#         (((mains_rank >= file2['Opening Rank']) & 
#           (mains_rank <= file2['Closing Rank']))|
#          (mains_rank <= file2['Opening Rank'])) & 
#         (seatty.upper() == file2['Seat Type']) & 
#         (file2['Gender'].isin(gender_list)) & 
#         (
#         (file2['Quota'] == 'OS') | 
#         (file2['Quota'] == 'AI') )
#     ]

#     choices_home = file2.loc[(mains_rank >= file2['Opening Rank']) &
#         (mains_rank <= file2['Closing Rank']) & 
#         (seatty.upper() == file2['Seat Type']) & 
#         (file2['Gender'].isin(gender_list)) &
#         (file2['Quota']== 'HS') &
#         (file2['Institute'].values[0] == home_state_institute)
#     ]

#     # Concatenate and sort the choices
#     choices_other = pd.concat([choices_home,choices_other])
#     choices = pd.concat([choices_iit, choices_other]).sort_values(by='Opening Rank')

# # Print the filtered choices without index  
#     choices['AcademicProgram'] = choices['Academic Program Name']
#     choices['OpeningRank'] = choices['Opening Rank']
#     choices['ClosingRank'] = choices['Closing Rank']
#     print( choices[['Institute', 'AcademicProgram','OpeningRank','ClosingRank']])
#     return choices[['Institute', 'AcademicProgram','OpeningRank','ClosingRank']].to_dict(orient='records')



import pandas as pd
import numpy as np
import os
from django.conf import settings

def get_choices_by_rank(adv_rank, mains_rank, seatty, gender, state, year):
    # Construct the full path to the CSV file
    file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
    file = pd.read_csv(file_path)
    file_path2 = os.path.join(settings.BASE_DIR, 'home', 'data', 'Seat_State_Matrix.csv')
    seats_file = pd.read_csv(file_path2)
    seats_file.dropna(subset=['Total (includes Female Supernumerary)'], inplace=True)

    # Filter IIT and non-IIT data for round 6 and year 2023
    file1 = file.loc[
        (file['Round'] == 6) & 
        (file['Year'] == year) & 
        ((file['Institute'].str.contains('Indian Institute  of Technology', case=False, na=False)) |
         (file['Institute'].str.contains('Indian Institute of Technology', case=False, na=False)))
    ]

    file2 = file.loc[
        (file['Round'] == 6) & 
        (file['Year'] == year) & 
        (~(file['Institute'].str.contains('Indian Institute  of Technology', case=False, na=False)))
    ]

    # Ensure the state is in uppercase
    state = state.upper()

    # Filter state quota from seats_file
    state_quota = seats_file.loc[seats_file['State/All India Seats'] == state]
    home_state_institute = state_quota['Institute Name']

    # Check if home_state_institute is empty
    if home_state_institute.empty:
        home_state_institute = pd.Series([])

    # Define gender list based on input
    gender_list = ['Female-only (including Supernumerary)'] if gender.lower() == 'female' else ['Gender-Neutral']

    # Convert ranks to numeric, coercing errors to NaN, and drop rows with NaN values in relevant columns
    for df in [file1, file2]:
        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df.dropna(subset=['Closing Rank', 'Institute'], inplace=True)
        df['Closing Rank'] = df['Closing Rank']

    # Filter choices for IITs
    choices_iit = file1.loc[
        (((adv_rank >= file1['Opening Rank']) & 
          (adv_rank <= file1['Closing Rank']))|
         (adv_rank <= file1['Opening Rank'])) & 
        (seatty.upper() == file1['Seat Type']) & 
        (file1['Gender'].isin(gender_list))
    ]

    # Filter choices for other institutes
    choices_other = file2.loc[
        (((mains_rank >= file2['Opening Rank']) & 
          (mains_rank <= file2['Closing Rank']))|
         (mains_rank <= file2['Opening Rank'])) & 
        (seatty.upper() == file2['Seat Type']) & 
        (file2['Gender'].isin(gender_list)) & 
        (
        (file2['Quota'] == 'OS') | 
        (file2['Quota'] == 'AI'))
    ]

    # Filter choices for home state quota
    if not home_state_institute.empty:
        choices_home = file2.loc[(mains_rank >= file2['Opening Rank']) &
            (mains_rank <= file2['Closing Rank']) & 
            (seatty.upper() == file2['Seat Type']) & 
            (file2['Gender'].isin(gender_list)) &
            (file2['Quota'] == 'HS') &
            (file2['Institute'].isin(home_state_institute))
        ]
        choices_other = pd.concat([choices_home, choices_other])
    else:
        choices_home = pd.DataFrame()

    # Concatenate and sort the choices
    choices = pd.concat([choices_iit, choices_other]).sort_values(by='Opening Rank')

    # Print the filtered choices without index  
    choices['AcademicProgram'] = choices['Academic Program Name']
    choices['OpeningRank'] = choices['Opening Rank']
    choices['ClosingRank'] = choices['Closing Rank']
    print(choices[['Institute', 'AcademicProgram','OpeningRank','ClosingRank']])
    return choices[['Institute', 'AcademicProgram','OpeningRank','ClosingRank']].to_dict(orient='records')