##2 Popular Branches
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Load the dataset
df = pd.read_csv('combined.csv')

# Ensure the relevant columns are present and convert ranks to numeric
df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')

# Drop rows with NaN values in 'Opening Rank' or 'Closing Rank'
df.dropna(subset=['Opening Rank', 'Closing Rank'], inplace=True)

# Calculate the rank difference and average rank
df['Rank Difference'] = df['Closing Rank'] - df['Opening Rank']
df['Average Rank'] = (df['Closing Rank'] + df['Opening Rank']) / 2

# Filter the dataset based on specific conditions
df_filtered = df.loc[(df['Gender'] == 'Gender-Neutral') & (df['Quota'] == 'AI') & 
                     (df['Seat Type'] == 'OPEN') & (df['Round'] == 6) & 
                     (df['Year'] == 2023) &
                     (~df['Institute'].str.contains('Architecture', na=False)) & 
                     (~df['Academic Program Name'].str.contains('Architecture', na=False))]

# Sort by Year (descending), then by Average Rank and Rank Difference (ascending)
sorted_by_popularity = df_filtered.sort_values(by=['Average Rank', 'Rank Difference'])

# Drop duplicates based on 'Academic Program Name' to get unique branches
df_unique_branches = sorted_by_popularity.drop_duplicates(subset='Academic Program Name', keep='first')

# Select the top 10 branches based on the sorted order
top_10 = df_unique_branches.head(10)

# Display the top 10 most popular branches
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
fig.update_layout(xaxis_title='Average Rank', yaxis_title='Academic Program Name', yaxis={'categoryorder':'total ascending'})
fig.show()

# If the data includes multiple years, perform trend analysis
top_institutes = df.loc[df['Year'] == 2023].groupby('Institute')['Average Rank'].mean().nsmallest(10).index.tolist()
df_filtered_all_years = df.loc[(df['Gender'] == 'Gender-Neutral') & (df['Quota'] == 'AI') & 
                               (df['Seat Type'] == 'OPEN') & (df['Round'] == 6) & 
                               (df['Institute'].isin(top_institutes)) & 
                               (df['Year'] >= 2016) & (df['Year'] <= 2023) &
                               (~df['Institute'].str.contains('Architecture', na=False)) & 
                               (~df['Academic Program Name'].str.contains('Architecture', na=False))]

if 'Year' in df.columns:
    trend_data = df_filtered_all_years[df_filtered_all_years['Academic Program Name'].isin(top_10['Academic Program Name'])]
    
    # Aggregate data to get average rank per year for each branch
    trend_data = trend_data.groupby(['Year', 'Academic Program Name']).agg({
        'Average Rank': 'mean'
    }).reset_index()

    # Create the figure for trend analysis using Plotly
    fig = go.Figure()

    for branch in top_10['Academic Program Name']:
        branch_data = trend_data[trend_data['Academic Program Name'] == branch]
        fig.add_trace(go.Scatter(
            x=branch_data['Year'],
            y=branch_data['Average Rank'],
            mode='lines+markers',
            name=f'{branch} - Average Rank',
            line=dict(width=2),  # Default line width
            opacity=0.8 # Default opacity
        ))

    fig.update_layout(
        title='Trend of Average Ranks Over Years for Top Branches',
        xaxis_title='Year',
        yaxis_title='Average Rank',
        yaxis_autorange='reversed',
        legend_title='Branches',
        hovermode='closest'
    )

    # Add custom hover effect to highlight only the hovered trace
    fig.update_layout(
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
        }]
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    fig.show()

# JavaScript for hover functionality
from IPython.display import display, HTML

hover_js = """
<script>
    var myPlot = document.getElementsByClassName('plotly-graph-div')[0];

    myPlot.on('plotly_hover', function(data){
        var index = data.points[0].curveNumber;
        Plotly.restyle(myPlot, 'opacity', Array.from({length: data.points.length}, (_, i) => i === index ? 1 : 0.2));
    });

    myPlot.on('plotly_unhover', function(data){
        Plotly.restyle(myPlot, 'opacity', 0.2);
    });
</script>
"""

display(HTML(hover_js))

responsive_js = """
<script>
    function resizePlot() {
        var plotDiv = document.getElementById('plotly-graph');
        var plotWidth = window.innerWidth * 0.8; // Adjust the percentage as needed
        Plotly.relayout(plotDiv, { width: plotWidth });
    }

    window.addEventListener('resize', resizePlot);
    // Initially resize the plot
    resizePlot();
</script>
"""

display(HTML(responsive_js))