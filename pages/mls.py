import streamlit as st
from streamlit_extras.colored_header import colored_header
import pandas as pd

st.title('Data Scouting Tool')
st.write('This tool allows you to filter and compare player data. All data, names & metrics are not based on real players.')

#######################
# Load Data
#######################

df = pd.read_csv('./mls_player_ratings.csv')

# Remove the currency symbol (£), commas, and the suffix (p/a)
df['Wage'] = df['Wage'].str.replace('£', '').str.replace(',', '').str.replace(' p/a', '')

# Convert the cleaned "Wage" column to a numerical type
df['Wage'] = pd.to_numeric(df['Wage'])

# Calculate the average Adjusted SABR Rating for each position
position_avg_ratings = df.groupby('Position')['Adjusted SABR Rating'].mean().round(2)

# Define min and max values
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
min_rating, max_rating = float(df['Average Rating'].min()), float(df['Average Rating'].max())
min_sabr, max_sabr = float(df['SABR Rating'].min()), float(df['SABR Rating'].max())
min_ad_rating, max_ad_rating = float(df['Adjusted Rating'].min()), float(df['Adjusted Rating'].max())
min_ad_sabr, max_ad_sabr = float(df['Adjusted SABR Rating'].min()), float(df['Adjusted SABR Rating'].max())

#######################
# Session State
#######################

# Session state variables
if 'player_search' not in st.session_state:
    st.session_state.player_search = ''
if 'position' not in st.session_state:
    st.session_state.position = []
if 'divisions' not in st.session_state:
    st.session_state.divisions = []
if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'seasons' not in st.session_state:
    st.session_state.seasons = []
if 'age' not in st.session_state:
    st.session_state.age = (min_age, max_age)
if 'rating' not in st.session_state:
    st.session_state.rating = (min_rating, max_rating)
if 'sabr' not in st.session_state:
    st.session_state.sabr = (min_sabr, max_sabr)
if 'ad_rating' not in st.session_state:
    st.session_state.ad_rating = (min_ad_rating, max_ad_rating)
if 'ad_sabr' not in st.session_state:
    st.session_state.ad_sabr = (min_ad_sabr, max_ad_sabr)

def reset_filters():
    st.session_state.player_search = ''
    st.session_state.position = []
    st.session_state.divisions = []
    st.session_state.teams = []
    st.session_state.seasons = []
    st.session_state.age = (min_age, max_age)
    st.session_state.rating = (min_rating, max_rating)
    st.session_state.sabr = (min_sabr, max_sabr)
    st.session_state.ad_rating = (min_ad_rating, max_ad_rating)
    st.session_state.ad_sabr = (min_ad_sabr, max_ad_sabr)

#######################
# Columns With Filters
#######################

# Three columns hold the filtering widgets
# Create columns with spaces in between
col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

with col1:
    player_search = st.text_input('Search by Player', key='player_search')
    position = st.multiselect('Select Position', options=['All'] + list(df['Position'].unique()), key='position')
    divisions = st.multiselect('Select Division', options=['All'] + list(df['Division'].unique()), key='divisions')
    teams = st.multiselect('Select Club', options=['All'] + list(df['Club'].unique()), key='teams')
    seasons = st.multiselect('Select Season', options=['All'] + list(df['Season'].unique()), key='seasons')
    st.button("Reset Filters", on_click=reset_filters, key='reset_filters_1')


with col3:
    age = st.slider('Filter by Age', min_value=min_age, max_value=max_age, key='age')
    rating = st.slider('Average Rating per Season', min_value=min_rating, max_value=max_rating, key='rating')
    sabr = st.slider('SABR Rating per Season', min_value=min_sabr, max_value=max_sabr, key='sabr')
    ad_rating = st.slider('Adjusted Rating (Mean Average Rating across all seasons)', min_value=min_ad_rating, max_value=max_ad_rating, key='ad_rating')
    ad_sabr = st.slider('Adjusted SABR Rating (Mean SABR Rating across all seasons)', min_value=min_ad_sabr, max_value=max_ad_sabr, key='ad_sabr')

# Filtering structure
filtered_df = df.copy()

if player_search:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(player_search, case=False, na=False)]

if 'All' not in position and position:
    filtered_df = filtered_df[filtered_df['Position'].isin(position)]

if 'All' not in divisions and divisions:
    filtered_df = filtered_df[filtered_df['Division'].isin(divisions)]

if 'All' not in teams and teams:
    filtered_df = filtered_df[filtered_df['Club'].isin(teams)]

if 'All' not in seasons and seasons:
    filtered_df = filtered_df[filtered_df['Season'].isin(seasons)]

filtered_df = filtered_df[
    (filtered_df['Age'].between(age[0], age[1])) &
    (filtered_df['Average Rating'].between(rating[0], rating[1])) &
    (filtered_df['SABR Rating'].between(sabr[0], sabr[1])) &
    (filtered_df['Adjusted Rating'].between(ad_rating[0], ad_rating[1])) &
    (filtered_df['Adjusted SABR Rating'].between(ad_sabr[0], ad_sabr[1]))
]

# Get the most recent season's data for each player
most_recent_season_df = df.loc[df.groupby('Name')['Season'].idxmax()]

# Get the list of filtered player names
filtered_players = ['Select'] + list(filtered_df['Name'].unique())

# Dictionary for position abbreviations
position_abbreviations = {
    'Central Attacking Midfielder': 'CAM',
    'Central Midfielder': 'CM',
    'Centre Back': 'CB',
    'Defensive Midfielder': 'DM',
    'Full Back': 'FB',
    'Striker': 'ST',
    'Wide Attacking Midfielder': 'AML/R',
    'Wing Back': 'WB',
    'Winger': 'WL/R',
}

with col2:
    with st.expander('Average Adjusted SABR Rating by Position', expanded=False):
        st.write("These are the mean Adjusted SABR Ratings for each position in the database. This is intended to give you an idea of the average rating for each position while providing context on what 'good' looks like.")
    # Display the average ratings for each position
    # Create columns dynamically
        columns = st.columns(4)
        
        # Iterate over the position_avg_ratings and place each in a column
        for idx, (position, avg_rating) in enumerate(position_avg_ratings.items()):
            col = columns[idx % 4]  # Cycle through the columns
            # Use the abbreviation if available, otherwise use the full position name
            short_position = position_abbreviations.get(position, position)
            col.metric(label=f"{short_position}", value=f"{avg_rating:.2f}")

    with st.expander('Compare Players', expanded=True):
        player1 = st.selectbox('Select Player 1', options=filtered_players)
        player2 = st.selectbox('Select Player 2', options=filtered_players)

        if player1 != 'Select' and player2 != 'Select':
            player1_data = most_recent_season_df[most_recent_season_df['Name'] == player1].iloc[0]
            player2_data = most_recent_season_df[most_recent_season_df['Name'] == player2].iloc[0]

            st.write("### Player Comparison")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**{player1}**")
                st.write(f"Age: {player1_data['Age']}")
                st.write(f"Position: {player1_data['Position']}")
                st.write(f"Club: {player1_data['Club']}")
                st.write(f"Wage: {player1_data['Wage']}")
                st.metric(label="Adjusted Rating", value=player1_data['Adjusted Rating'])
                st.metric(label="Adjusted SABR Rating", value=player1_data['Adjusted SABR Rating'])

            with col2:
                st.write(f"**{player2}**")
                st.write(f"Age: {player2_data['Age']}")
                st.write(f"Position: {player2_data['Position']}")
                st.write(f"Club: {player2_data['Club']}")
                st.write(f"Wage: {player2_data['Wage']}")
                st.metric(label="Adjusted Rating", value=player2_data['Adjusted Rating'])
                st.metric(label="Adjusted SABR Rating", value=player2_data['Adjusted SABR Rating'])

#######################
# Dataframe Display
#######################

colored_header(
    label='Full Database',
    description='All metrics & new ratings for players in the MLS',
    color_name='orange-70',
    )

# Convert the Season column to string to avoid comma formatting
filtered_df['Season'] = filtered_df['Season'].astype(str)

# Display the dataframe
with st.expander('Table Of Full Data', expanded=True):
    st.data_editor(filtered_df)

    # Shows the number of records displayed & explainer message
    st.write(f'Showing {len(filtered_df)} out of {len(df)} records. These records can be downloaded as a CSV file. Hover over the dataframe.')

colored_header(
    label='Finding Value',
    description='Scatterplot comparing player wages to their Adjusted SABR Ratings',
    color_name='orange-70',
    )

with st.expander('Wage vs SABR Rating Scatterplot', expanded=False):
    # Scatter plot using filtered_df
    st.vega_lite_chart(
        filtered_df,
        {
            "mark": {"type": "circle", "tooltip": True, "size": 100},  # Set size to make points bigger
            "encoding": {
                "x": {"field": "Adjusted SABR Rating", "type": "quantitative"},
                "y": {"field": "Wage", "type": "quantitative"},
                "color": {"field": "Position", "type": "nominal"},
                "tooltip": [
                    {"field": "Name", "type": "nominal"},
                    {"field": "Club", "type": "nominal"},
                    {"field": "Wage", "type": "quantitative"},
                    {"field": "Adjusted SABR Rating", "type": "quantitative"},
                    {"field": "Position", "type": "nominal"}
                ]
            },
        },
        theme="streamlit",
        use_container_width=True
    )
