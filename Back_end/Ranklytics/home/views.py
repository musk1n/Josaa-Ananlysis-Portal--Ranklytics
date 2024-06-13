from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from django.templatetags.static import static
from django.urls import path

def home(request):
     
    return render(request , 'home.html')

def about(request):
     
    return render(request , 'about.html')

def slider(request):
     
    return render(request , 'slider.html')

def q1(request):
     
    return render(request , 'q1.html')

#1 CHOICES


import json

from django.http import JsonResponse
from home.utils import get_choices_by_rank

def display_choices(request):
    if request.method == 'GET':
        adv_rank = request.GET.get('adv_rank')
        mains_rank = request.GET.get('mains_rank')
        seatty = request.GET.get('seatty')
        gender = request.GET.get('gender')
        state = request.GET.get('state')
        year = request.GET.get('year')

        
        try:
            if (adv_rank=="NA"): adv_rank=10000000000000000
            adv_rank = int(adv_rank) if adv_rank else None
            mains_rank = int(mains_rank) if mains_rank else None
            year = int(year) if year else None
        except ValueError:
            return render(request, 'choices.html', {'error': 'Invalid rank provided'})

        if adv_rank is None or mains_rank is None:
            return render(request, 'choices.html', {'error': 'Both ranks are required'})

       
        choices = get_choices_by_rank(adv_rank, mains_rank, seatty, gender, state, year)

        
        return render(request, 'choices.html', {'choices': choices})

def get_college_data(request):
    data = {
        "message": "College data",
        "data": []
    }
    return JsonResponse(data)

# 2 Popular_branches


from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from django.conf import settings


def plot_graph(request):
  
    file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
    df = pd.read_csv(file_path)
   
    df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
    
   
    df.dropna(subset=['Opening Rank', 'Closing Rank'], inplace=True)

    
    df['Rank Difference'] = df['Closing Rank'] - df['Opening Rank']
    df['Average Rank'] = (df['Closing Rank'] + df['Opening Rank']) / 2

    
    df_filtered = df.loc[(df['Gender'] == 'Gender-Neutral') & (df['Quota'] == 'AI') & 
                     (df['Seat Type'] == 'OPEN') & (df['Round'] == 6) & 
                     (df['Year'] == 2023) &
                     (~df['Institute'].str.contains('Architecture', na=False)) & 
                     (~df['Academic Program Name'].str.contains('Architecture', na=False))]

    
    sorted_by_popularity = df_filtered.sort_values(by=['Average Rank', 'Rank Difference'])

  
    df_unique_branches = sorted_by_popularity.drop_duplicates(subset='Academic Program Name', keep='first')

    
    top_10 = df_unique_branches.head(10)

    print("Top 10 Most Popular Branches Based on Rank Difference:")
    print(top_10['Academic Program Name'])

    fig = px.bar(
        top_10,
        x='Average Rank',
        y='Academic Program Name',
        orientation='h',
        title='Average Rank of Top 10 Different Branches',
        labels={'Average Rank': 'Average Rank', 'Academic Program Name': 'Academic Program Name'},
        color='Average Rank',
        color_continuous_scale=px.colors.sequential.Greens
    )
    fig.update_layout(
        xaxis_title='Average Rank',
        yaxis_title='Academic Program Name',
        yaxis={'categoryorder':'total descending'},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Courier New, monospace", size=14, color="#FFFFFF"),  # Change the font
        title=dict(text='Average Rank of Top 10 Different Branches', font=dict(size=30, color='#FFFFFF', family='Courier New, monospace', weight='bold')),  # Bold and larger title
          # Smaller legend font
        legend=dict(font=dict(size=10, color='#FFFFFF')),  # Smaller legend font with white color
        margin=dict(l=20, r=50, t=100, b=50),  # Adjust margins to allow more space for the plot
        width=1400,  # Increase figure width
        height=600, 
        autosize=True,
       
    
        
        )
    fig.to_html()
    graph_html = fig.to_html(full_html=False)

    top_institutes = df.loc[df['Year'] == 2023].groupby('Institute')['Average Rank'].mean().nsmallest(10).index.tolist()
    df_filtered_all_years = df.loc[(df['Gender'] == 'Gender-Neutral') & (df['Quota'] == 'AI') & 
                                    (df['Seat Type'] == 'OPEN') & (df['Round'] == 6) & 
                                    (df['Institute'].isin(top_institutes)) & 
                                    (df['Year'] >= 2016) & (df['Year'] <= 2023) &
                                    (~df['Institute'].str.contains('Architecture', na=False)) & 
                                    (~df['Academic Program Name'].str.contains('Architecture', na=False))]

    if 'Year' in df.columns:
            trend_data = df_filtered_all_years[df_filtered_all_years['Academic Program Name'].isin(top_10['Academic Program Name'])]
            
            
            trend_data = trend_data.groupby(['Year', 'Academic Program Name']).agg({
                'Average Rank': 'mean'
            }).reset_index()

    trend_fig = go.Figure()

    for branch in top_10['Academic Program Name']:
            branch_data = trend_data[trend_data['Academic Program Name'] == branch]
            trend_fig.add_trace(go.Scatter(
                x=branch_data['Year'],
                y=branch_data['Average Rank'],
                mode='lines+markers',
                name=f'{branch} - Average Rank',
                line=dict(width=2),  
                opacity=0.8 
            ))

    trend_fig.update_layout(
            title='Trend of Average Ranks Over Years for Top Branches',
            xaxis_title='Year',
            yaxis_title='Average Rank',
            yaxis_autorange='reversed',
            legend_title='Branches',
            hovermode='closest'
        )

       
    trend_fig.update_layout(
            updatemenus=[{
                "buttons": [
                    {
                        "args": ["mode", "lines+markers"],
                        "label": "Show All",
                        "method": "restyle"
                    }
                ],
                "direction": "down",
                "showactive": True
            }],
            paper_bgcolor='rgba(0,0,0,0)',  
        font=dict(family="Courier New, monospace", size=14, color="#FFFFFF"),  # Change the font
        title=dict(text='Average Rank of Top 10 Different Branches', font=dict(size=30, color='#FFFFFF', family='Courier New, monospace', weight='bold')),  # Bold and larger title
          # Smaller legend font
        legend=dict(font=dict(size=10, color='#FFFFFF')),  # Smaller legend font with white color
        margin=dict(l=20, r=50, t=100, b=50),  # Adjust margins to allow more space for the plot
        width=1400,  # Increase figure width
        height=600,
        autosize=True,
       


            
        )
    trend_fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            
            plot_bgcolor='rgba(0,0,0,0)',
        )

    trend_graph_html = trend_fig.to_html(full_html=False)
   
    

    return render(request, 'popular_branches.html', {'graph': graph_html, 'trend_graph': trend_graph_html})





## 3 college wise popular branch

from django.shortcuts import render
import pandas as pd
import plotly.express as px
import os
from django.conf import settings

def college_branch_popularity(request):
    if request.method == 'POST':
        college_name = request.POST.get('college_name')

      
        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
        df = pd.read_csv(file_path)

       
        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df.dropna(subset=['Closing Rank'], inplace=True)

        college_data = df.loc[(df['Gender'] == 'Gender-Neutral') &
                             ((df['Quota'] == 'AI') | (df['Quota'] == 'OS')) &
                             (df['Seat Type'] == 'OPEN') & 
                             (df['Round'] == 6) & 
                             (df['Year'] == 2023) &
                             (df['Institute'] == college_name)]

        college_data['Average Rank'] = (college_data['Opening Rank'] + college_data['Closing Rank']) / 2

        college_data = college_data[['Academic Program Name', 'Average Rank']]
        sorted_college_data = college_data.sort_values(by='Average Rank')
        top_10 = sorted_college_data.head(10)

        fig = px.bar(
            top_10,
            x='Average Rank',
            y='Academic Program Name',
            orientation='h',
            title=f'Average Rank of Top 10 Different Branches in {college_name}',
            labels={'Average Rank': 'Average Rank', 'Academic Program Name': 'Academic Program Name'},
            color='Average Rank',
            color_continuous_scale=px.colors.sequential.Greens
        )
        fig.update_layout(
          
    xaxis_title='Average Rank',
    yaxis_title='Academic Program Name',
    yaxis={'categoryorder': 'total descending'},
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
    font=dict(family="Courier New, monospace", size=14, color="#FFFFFF"),  # Change the font
    title=dict(text=f'Average Rank of Top 10 Different Branches in {college_name}', font=dict(size=25, color='#FFFFFF', family='Courier New, monospace', weight='bold')),  # Bold and larger title
    legend=dict(font=dict(size=10, color='#FFFFFF')),  # Smaller legend font with white color
    margin=dict(l=20, r=50, t=100, b=50),  # Adjust margins to allow more space for the plot
    width=1400,  # Increase figure width
    height=600,  # Increase figure height
)


        graph_html = fig.to_html(full_html=False)

        return render(request, 'college_popular_branch.html', {'graph': graph_html, 'college_name': college_name})
    else:
        return render(request, 'college_popular_branch.html')
    


##4 branchwise college priority

from django.shortcuts import render
import pandas as pd
import plotly.express as px
import os
from django.conf import settings

def branch_college_popularity(request):

    dtype_dict = {
        'Opening Rank': 'str',
        'Closing Rank': 'str',
        'Academic Program Name': 'str',
        'Seat Type': 'str',
        'Gender': 'str',
        'Quota': 'str',
        'Institute': 'str',
        'Round': 'int',
        'Year': 'int'
    }

    if request.method == 'POST':
        branch = request.POST.get('branch')
        try:
            
            rank_adv = request.POST.get('rank_adv')
            if (rank_adv=="NA"): rank_adv=1000000000000000
            rank_adv = int(rank_adv)
            rank_mains = int(request.POST.get('rank_mains'))
        except ValueError:
            return render(request, 'branchwise_college.html', {'error': 'Please enter valid ranks.'})

        seatty = request.POST.get('seatty').upper()
        gender = request.POST.get('gender').lower()
        quota = request.POST.get('quota').upper()

        gender_list = ['Female-only (including Supernumerary)'] if gender.lower() == 'female' else ['Gender-Neutral']

        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
        df = pd.read_csv(file_path)

        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df.dropna(subset=['Closing Rank'], inplace=True)

        df['Average Rank'] = (df['Closing Rank'] + df['Opening Rank']) / 2

        escaped_branch = branch.replace("(", "\\(").replace(")", "\\)")
        college_data = df[(df['Academic Program Name'].str.contains(escaped_branch, case=False)) &
                          (df['Seat Type'] == seatty) &
                          (df['Gender'].isin(gender_list)) &
                          (df['Quota'] == quota) &
                          (df['Round'] == 6) &
                          (df['Year'] == 2023)]

        iit_data = college_data[
            (((college_data['Opening Rank'] <= rank_adv) & (college_data['Closing Rank'] >= rank_adv)) | 
            (college_data['Opening Rank'] >= rank_adv)) & 
            ((college_data['Institute'].str.contains('Indian Institute of Technology', case=False)))
        ]

        non_iit_data = college_data[
            (((college_data['Opening Rank'] <= rank_mains) & (college_data['Closing Rank'] >= rank_mains)) | 
            (college_data['Opening Rank'] >= rank_mains)) & 
            (~college_data['Institute'].str.contains('Indian Institute of Technology', case=False))
        ]

        combined_2023 = pd.concat([iit_data, non_iit_data])

        top_10 = combined_2023.sort_values(by='Average Rank').head(10)

        top_10['Institute-Academic Program Name'] = top_10['Institute'] + ' - ' + top_10['Academic Program Name']

        fig = px.bar(
            top_10,
            x='Average Rank',
            y='Institute-Academic Program Name',
            orientation='h',
            title=f'Average Rank of Top 10 Different Colleges offering {branch}',
            labels={'Average Rank': 'Average Rank', 'Institute-Academic Program Name': 'Institute-Academic Program Name'},
            color='Average Rank',
            color_continuous_scale=px.colors.sequential.Greens
        )

        fig.update_layout(
            xaxis_title='Average Rank',
            yaxis_title='Institute-Academic Program Name',
            yaxis={'categoryorder': 'total descending'},
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(family="Courier New, monospace", size=14, color="#FFFFFF"),
            title=dict(text=f'Average Rank of Top 10 Different Colleges offering {branch}', font=dict(size=25, color='#FFFFFF', family='Courier New, monospace', weight='bold')),
            legend=dict(font=dict(size=10, color='#FFFFFF')),
            margin=dict(l=20, r=50, t=100, b=50),
            width=1400,
            height=600,
            autosize=True,
        )

        graph_html = fig.to_html(full_html=False)

        return render(request, 'branchwise_college.html', {'graph': graph_html, 'branch': branch})
    else:
        return render(request, 'branchwise_college.html')


    
##5 branch and college trend over years

from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
import os
from django.conf import settings

def branch_college_trend(request):

    dtype_dict = {
        'Opening Rank': 'str',
        'Closing Rank': 'str',
        'Academic Program Name': 'str',
        'Seat Type': 'str',
        'Gender': 'str',
        'Quota': 'str',
        'Institute': 'str',
        'Round': 'int',
        'Year': 'int'
    }

    if request.method == 'POST':
        college_name = request.POST.get('college_name')
        branch = request.POST.get('branch')
        seatty = request.POST.get('seatty').upper()
        gender = request.POST.get('gender').lower()
        quota = request.POST.get('quota').upper()

        gender_list = ['Female-only (including Supernumerary)'] if gender.lower() == 'female' else ['Gender-Neutral']

        
        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
        df = pd.read_csv(file_path)

       
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df.dropna(subset=['Closing Rank', 'Opening Rank'], inplace=True)

        escaped_branch = branch.replace("(", "\\(").replace(")", "\\)")
        df['Average Rank']=(df['Opening Rank']+df['Closing Rank'])/2
        round_data = df[(df['Institute'] == college_name) & 
                          (df['Seat Type'] == seatty) & 
                          (df['Gender'].isin(gender_list)) & 
                          (df['Quota'] == quota) & 
                          (df['Year'] == 2023) & 
                          (df['Academic Program Name'].str.contains(escaped_branch, case=False))]
        college_data = df[(df['Institute'] == college_name) & 
                          (df['Seat Type'] == seatty) & 
                          (df['Gender'].isin(gender_list)) & 
                          (df['Quota'] == quota) & 
                          (df['Round'] == 6) & 
                          (df['Academic Program Name'].str.contains(escaped_branch, case=False))]
        
      
        college_data = college_data.sort_values(by='Year')
        round_data = round_data.sort_values(by='Round')
        fig = go.Figure()
        fig2 = go.Figure()

        
        fig.add_trace(go.Scatter(
            x=college_data['Year'],
            y=college_data['Average Rank'],
            mode='lines+markers',
            marker=dict(size=8),
            line=dict(color='orange',width=3),
            name=f'{branch} - {college_name}'
        ))

       
        fig.update_layout(
            title=f"Average Rank of {branch} in {college_name}",
            xaxis_title='Years',
            yaxis_title='Average Rank',
            xaxis=dict(tickmode='linear', tick0=2018, dtick=1),
            yaxis=dict(autorange='reversed'),
            autosize=True,  # Enable Plotly's responsive layout
            plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
            paper_bgcolor='rgba(0,0,0,0)',
             font=dict(color='white', size=16),  # Set font color to white and increase font size
            legend=dict(font=dict(color='white', size=14)), 
            width= 1300,
            height= 500,
        )

        fig2.add_trace(go.Scatter(
            x=round_data['Round'],
            y=round_data['Closing Rank'],
            mode='lines+markers',
            marker=dict(size=8),
            line=dict(color='orange',width=3),
            name=f'{branch} - {college_name}'
        ))

       
        fig2.update_layout(
            title=f"Closing Rank of {branch} in {college_name}",
            xaxis_title='Round',
            yaxis_title='Closing Rank',
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            yaxis=dict(autorange='reversed'),
            autosize=True,  # Enable Plotly's responsive layout
            plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color to transparent
            paper_bgcolor='rgba(0,0,0,0)',
             font=dict(color='white', size=16),  # Set font color to white and increase font size
            legend=dict(font=dict(color='white', size=14)), 
            width= 1300,
            height= 500,
        )

        graph_html = fig.to_html(full_html=False)
        round_graph_html = fig2.to_html(full_html=False)
        
        return render(request, 'branch_college_trend.html', {'graph': graph_html, 'round_graph': round_graph_html, 'branch': branch, 'college_name': college_name})
    else:
        return render(request, 'branch_college_trend.html')
    


##6 new branch trend 
from django.shortcuts import render
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from django.conf import settings

def new_branches_popularity(request):
    if request.method == 'POST':
        rank_adv = request.POST.get('rank_adv')
        if (rank_adv=="NA"): rank_adv=100000000000000000
        rank_adv=int(rank_adv)
        rank_mains = int(request.POST.get('rank_mains'))
        seatty = request.POST.get('seatty').upper()
        gender = request.POST.get('gender').lower()
        quota = request.POST.get('quota').upper()

        gender_list = ['Female-only (including Supernumerary)'] if gender == 'female' else ['Gender-Neutral']

        # Load the dataset
        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'combined.csv')
        df = pd.read_csv(file_path)
        df['Academic Program Name-Institute'] = df['Academic Program Name'] + ' - ' + df['Institute']

        # Ensure the relevant columns are present and convert ranks to numeric
        df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
        df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
        df.dropna(subset=['Opening Rank', 'Closing Rank'], inplace=True)

        df['Average Rank'] = (df['Closing Rank'] + df['Opening Rank']) / 2

        # Filter data based on rank inputs
        iit_data = df[(((df['Closing Rank'] >= rank_adv) & (rank_adv >= df['Opening Rank']))| (rank_adv <= df['Opening Rank'])) & ((df['Institute'].str.contains('Indian Institute  of Technology'))|(df['Institute'].str.contains('Indian Institute  of Technology')))]
        non_iit_data = df[(((df['Closing Rank'] >= rank_mains) & (rank_mains >= df['Opening Rank']))| (rank_mains <= df['Opening Rank'])) & (~df['Institute'].str.contains('Indian Institute  of Technology'))]

        df_filtered = pd.concat([iit_data, non_iit_data])

        # Filter the dataset based on specific conditions
        df_filtered = df_filtered.loc[
            (df_filtered['Gender'].str.contains('|'.join(gender_list))) &
            (df_filtered['Quota'] == quota) &
            (df_filtered['Seat Type'] == seatty) &
            (df_filtered['Round'] == 6) &
            (~df_filtered['Institute'].str.contains('Architecture', na=False)) &
            (~df_filtered['Academic Program Name'].str.contains('Architecture', na=False))
        ]

        # Identify unique branches from the filtered data
        df_unique_branches = df_filtered.drop_duplicates(subset='Academic Program Name')['Academic Program Name']

        # Identify new branches introduced after 2019
        new_branches = pd.DataFrame()

        for branch in df_unique_branches:
            df_branch = df_filtered[df_filtered['Academic Program Name'] == branch]
            if df_branch['Year'].min() > 2019:
                new_branches = pd.concat([new_branches, df_branch])
                 
        

        # Sort by average rank
        sorted_by_popularity = new_branches.sort_values(by='Average Rank')

        # Select the top 10 branches based on the sorted order
        top_10 = sorted_by_popularity.drop_duplicates(subset=['Academic Program Name', 'Institute']).head(10)

        # Create the bar chart
        fig1 = go.Figure()

        fig1.add_trace(go.Bar(
            x=top_10['Average Rank'],
            y=top_10['Academic Program Name-Institute'],
            orientation='h',
            marker=dict(color=top_10['Average Rank'], coloraxis="coloraxis")
        ))

        fig1.update_layout(
            xaxis_title='Average Rank',
            yaxis_title='Academic Program Name-Institute',
            yaxis=dict(autorange='reversed'),
            coloraxis=dict(colorscale='Greens'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Courier New, monospace",size=14 ,color='white'),
            title=dict(text='Average Rank of Top 10 Different Branches', font=dict(size=25, color='#FFFFFF', family='Courier New, monospace', weight='bold')),
                       
            legend=dict(
                font=dict(size=8,color='white'),
                bgcolor='rgba(0,0,0,0)',
            ),
            margin=dict(l=20, r=50, t=100, b=50),
            width=1400,
            height=600,
            autosize=True,
        )

        # Convert the bar chart to HTML
        bar_chart_html = fig1.to_html(full_html=False)

        # Create the trend analysis plot if the data includes multiple years
        fig2 = go.Figure()

        if 'Year' in df.columns:
            trend_data = df_filtered[df_filtered['Academic Program Name'].isin(top_10['Academic Program Name'])]

            for branch in top_10['Academic Program Name-Institute']:
                branch_data = trend_data[trend_data['Academic Program Name-Institute'] == branch]
                fig2.add_trace(go.Scatter(
                    x=branch_data['Year'],
                    y=branch_data['Average Rank'],
                    mode='lines+markers',
                    name=f'{branch} - Average Rank'
                ))

            fig2.update_layout(
                title=dict(text='Trend of Average Ranks Over Years for Top New Branches', font=dict(size=25, color='#FFFFFF', family='Courier New, monospace', weight='bold')),
                xaxis_title='Year',
                yaxis_title='Average Rank',
                legend_title='Branches',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family="Courier New, monospace"),
                legend=dict(
                    font=dict(color='white'),
                    bgcolor='rgba(0,0,0,0)'
                ),
                margin=dict(l=100, r=20, t=50, b=50),
                width=1800,
                height=400,
                autosize=True,
            )
            fig2.update_xaxes(range=[2020, 2023])

        # Convert the trend plot to HTML
        trend_plot_html = fig2.to_html(full_html=False)

        return render(request, 'new_branches_popularity.html', {
            'bar_chart': bar_chart_html,
            'trend_plot': trend_plot_html
        })
    else:
        return render(request, 'new_branches_popularity.html')


##8 Prediction 

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from home.forms import PreferenceForm
import os

def generate_preference_list(file_path, rank, seat_type, quota, exam, gender):
    # Load the CSV file
    try:
        file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'Updated_Predicted_Data2.csv')
        df = pd.read_csv(file_path)
        df['Predicted_Opening_Rank'] = pd.to_numeric(df['Predicted_Opening_Rank'], errors='coerce')
        df['Predicted_Closing_Rank'] = pd.to_numeric(df['Predicted_Closing_Rank'], errors='coerce')
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
              (df['Predicted_Closing_Rank'] >= rank))) &
              (df['Predicted_Closing_Rank'] >= df['Predicted_Opening_Rank']) &
              (df['Predicted_Opening_Rank'] >0)
        ]
    except Exception as e:
        print(f"Error filtering data: {e}")
        return pd.DataFrame()

    # Check if any data remains after filtering
    if filtered_df.empty:
        print("No matching data found for the given criteria.")
        return pd.DataFrame()

    # Sort the data by round and predicted opening rank
    sorted_df = filtered_df.sort_values(by=['Round', 'Predicted_Opening_Rank'])

    return sorted_df

def preference_view(request):
    if request.method == 'POST':
        form = PreferenceForm(request.POST)
        if form.is_valid():
            file_path = 'preference_project/Updated_Predicted_Data2.csv'
            rank = form.cleaned_data['rank']
            seat_type = form.cleaned_data['seat_type']
            quota = form.cleaned_data['quota']
            exam = form.cleaned_data['exam']
            gender = form.cleaned_data['gender']

            sorted_df = generate_preference_list(file_path, rank, seat_type, quota, exam, gender)

            if not sorted_df.empty:
                rounds = sorted_df['Round'].unique()
                round_data = {round_num: sorted_df[sorted_df['Round'] == round_num].to_dict('records') for round_num in rounds}
                return render(request, 'preference_app/results.html', {'round_data': round_data})
            else:
                return HttpResponse("No data to display.")
    else:
        form = PreferenceForm()

    return render(request, 'preference_app/index.html', {'form': form})