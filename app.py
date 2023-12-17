import pandas as pd
import streamlit as st
import pandas as pd
import preprocess,filter_csv
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region = pd.read_csv('noc_regions.csv')
df = filter_csv.preprocess(df,region)

st.title("GAME OF MEDALS 🏅")
st.sidebar.title('Exploring Olympic History')

user_input = st.sidebar.radio(
    'Select an Option',
    ('Overall Analysis','Country-wise Analysis','Athlete wise Analysis','Medal Tally',)
)

if user_input=='Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    statistics = {
        "Editions": editions,
        "Hosts": cities,
        "Sports": sports,
        "Events": events,
        "Nations": nations,
        "Athletes": athletes,
    }
    st.title("Top Statistics")

    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.subheader("Editions")
        st.info(statistics["Editions"])

    with row1_col2:
        st.subheader("Hosts")
        st.success(statistics["Hosts"])

    with row1_col3:
        st.subheader("Sports")
        st.warning(statistics["Sports"])

    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.subheader("Events")
        st.error(statistics["Events"])

    with row2_col2:
        st.subheader("Nations")
        st.info(statistics["Nations"])

    with row2_col3:
        st.subheader("Athletes")
        st.success(statistics["Athletes"])

    nations_over_time = preprocess.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = preprocess.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)
    
    athlete_over_time = preprocess.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)
    
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = preprocess.most_successful(df, selected_sport)
    st.table(x)


if user_input == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = preprocess.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(" Medal Tally of " +selected_country)
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = preprocess.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = preprocess.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_input == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    # st.title('Height Vs Weight')
    # selected_sport = st.selectbox('Select a Sport', sport_list)
    # temp_df = preprocess.weight_v_height(df,selected_sport)
    # fig,ax = plt.subplots()
    # ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    # st.pyplot(fig)

    # st.title("Men Vs Women Participation Over the Years")
    # final = preprocess.men_vs_women(df)
    # fig = px.line(final, x="Year", y=["Male", "Female"])
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.plotly_chart(fig)


if user_input == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = preprocess.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = preprocess.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.text("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.text("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.text(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.text(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)