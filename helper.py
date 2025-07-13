import numpy as np

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['total']=medal_tally['total'].astype('int')


    return medal_tally


def country_year_list(df):
    year=df['Year'].unique().tolist()
    year.sort()
    year.insert(0,'Overall')

    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return year,country


def fetch_year_country(df,year,country):
    medal_df= df.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year =='Overall' and country == 'Overall':
        temp_df=medal_df
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        temp_df=medal_df[(medal_df['Year']==int(year))  & (medal_df['region']==country)] 
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']

    return x



def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Editions','count':col},inplace=True)

    return nations_over_time



def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!= 'Overall':
        temp_df=temp_df[temp_df['Sport']==sport]

    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df)[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Total_Medals'},inplace=True)
    return x


def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Year','NOC','Games','Sport','Year','Event','Medal','City'],inplace=True)

    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df
def country_event_heatmap(df,country):
     temp_df=df.dropna(subset=['Medal'])
     temp_df.drop_duplicates(subset=['Year','NOC','Games','Sport','Year','Event','Medal','City'],inplace=True)

     new_df=temp_df[temp_df['region']==country]
     pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
     return pt


def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])   
    temp_df=temp_df[temp_df['region']==country]
    x =  temp_df['Name'].value_counts().reset_index().head(10).merge(df,how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'count':'total_medals'},inplace=True)
    return x

def height_v_weight(df,sport):
    player_df=df.drop_duplicates(subset=['Name','region'])
    player_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':

        temp_df=player_df[player_df['Sport']==sport]
        return temp_df
    else:
        return player_df
    


def men_vs_women(df):
    player_df=df.drop_duplicates(subset=['Name','region'])
    men=player_df[player_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=player_df[player_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final=men.merge(women,on='Year',how='left').fillna(0).astype('int')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    return final