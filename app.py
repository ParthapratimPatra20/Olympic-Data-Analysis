import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.figure_factory as ff


df=pd.read_csv('E:/datasets/athlete_events.csv')
region_df=pd.read_csv('E:/datasets/noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis by Parthapratim Patra")
st.sidebar.image("download (1).jpeg")

user_menu=st.sidebar.radio(

    'Select an option',
    ('Medal Tally','Overall Analysis','Coumtry-wise analysis','Athlete-wise analysis')
)



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",year)
    selected_country=st.sidebar.selectbox("Select Country",country)

    medal_tally=helper.fetch_year_country(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")

    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in"  + str(selected_year)+ " Olympics")

    if selected_year=='Overall' and selected_country!='Overall':
        st.title("Medal Tally of " +str(selected_country) + " Olympics" )
    if selected_year!='Overall' and selected_country!='Overall':
        st.title("Medal Tally in  " +str(selected_year) +"of" +str(selected_country)+" Olympics")
    st.table(medal_tally)



if user_menu == "Overall Analysis":
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)


    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)
        
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    st.title("Participating Nations Over Year")
    nations_over_time=helper.data_over_time(df,'region')
    fig=px.line(nations_over_time,x='Editions',y='region')
    st.plotly_chart(fig)

    st.title("Events Over Year")
    event_over_time=helper.data_over_time(df,'Event')
    fig=px.line(event_over_time,x='Editions',y='Event')
    st.plotly_chart(fig)

    st.title("Athletes Over Year")
    athlete_over_time=helper.data_over_time(df,'Name')
    fig=px.line(athlete_over_time,x='Editions',y='Name')
    st.plotly_chart(fig)

    st.title('No. of Events Over Time (Each Sport)')
    fig,ax=plt.subplots(figsize=(25,25))
    x=df.drop_duplicates(['Year','Event','Sport'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns="Year",values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select a Sport",sport_list)
    p=helper.most_successful(df,selected_sport)
    st.table(p)

if user_menu=='Coumtry-wise analysis':
    st.sidebar.title("Country-wise analysis")
    country_list=np.unique(df['region'].dropna().values).tolist()
    country_list.sort()
    select_country=st.sidebar.selectbox("select country",country_list)
    st.title("Medal Tally over the years")
    country_df=helper.yearwise_medal_tally(df,select_country)
    fig=px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)
    st.title( select_country +" excels in the following sports")
    pt=helper.country_event_heatmap(df,select_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    st.title("Top 10 athletes of " +select_country)
    top10_df=helper.most_successful_countrywise(df,select_country)
    st.table(top10_df)


if user_menu =='Athlete-wise analysis':
    
    player_df=df.drop_duplicates(subset=['Name','region'])
    x1=player_df['Age'].dropna().astype('int')
    x2=player_df[player_df['Medal']=='Gold']['Age'].dropna().astype('int')
    x3=player_df[player_df['Medal']=='Silver']['Age'].dropna().astype('int')
    x4=player_df[player_df['Medal']=='Bronze']['Age'].dropna().astype('int')
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of age ")
    st.plotly_chart(fig)

    st.title("Height vs Weight")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox("Select a Sport",sport_list)

    temp_df=helper.height_v_weight(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(player_df,x='Weight',y='Height',hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    
    st.pyplot(fig)
    st.title("Male vs Female participants over the Years")
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
