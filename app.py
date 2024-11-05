import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions_app import *
pd.options.display.max_colwidth = None


# **************  load the files  ***************************************
# load info 
infos_show = pd.read_csv('C:\Users\danal\Documents\Data Science\DataScience Bootcamp\10_Project\Code/Ergebnisse/app/infos_show.csv')
infos_show = infos_show.drop('Unnamed: 0', axis = 1)


# check if already there
if ~st.session_state.posts:
    st.session_state.posts = pd.read('dfsdfsdf')
    
# load posts
# load posts in chunks of 50000 to save memory
posts = []
with pd.read_csv('C:\Users\danal\Documents\Data Science\DataScience Bootcamp\10_Project\Code/Ergebnisse/app/posts_show.csv', chunksize=50000) as reader:
    for chunk in reader:
        chunk = change_types(chunk)
        posts.append(chunk)
# reset index of posts dataframes
for i in range(0,len(posts)):
    posts[i] = posts[i].set_index('Unnamed: 0')
    # delete the name of the index
    posts[i].index.name = None

# load election results
elections = pd.read_csv('C:\Users\danal\Documents\Data Science\DataScience Bootcamp\10_Project\Code/Ergebnisse/election2021.csv')
elections = elections.drop('Unnamed: 0', axis = 1)



#***** Create a sidebar for options ************************* 
# Sidebar options
st.sidebar.header("Options")

# multiselection of parties
with st.sidebar:
    # ************choose party****************
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    parties = st.multiselect('Select parties:',
                             ['All','SPD', 'GRÜNE', 'CSU', 'CDU', 'AfD', 'FDP', 'DIE LINKE', 'SSW'],
                            default='All')
    #  select all parties if 'all' is selected
    if 'All' in parties:
        parties = ['SPD', 'GRÜNE', 'CSU', 'CDU', 'AfD', 'FDP', 'DIE LINKE', 'SSW']
    # show selected parties
    st.sidebar.write(f'You selected: {str(parties).replace('[','').replace(']','').replace("'","")}')
    # create mask for selected parties
    mask_parties = infos_show['party'].isin(parties)

    # ************choose politician****************
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    # selection of a politician
    # Text area
    mask_pol =[]
    politician = st.text_area(label='Choose a politician to be analyzed & Ctrl+Enter',
                              value=None, placeholder= 'Enter one politican here\nType in the name as stated in the tables')
    if politician in list(infos_show['name']):
        st.write(f'You entered: {politician}')
        for i in range(0,len(posts)):
            mask_pol.append(posts[i]['name'] == politician)
    elif politician is None:
        st.write('')
        # make a mask with every entry = True
        for i in range(0,len(posts)):
            mask_pol.append(posts[i]['name'] == posts[i]['name'])
    elif politician not in list(infos_show['name']):
        st.write('You have a typo!')

# ************choose a date ****************
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    # selection of a politician
    # Text area
    mask_date_max =[]
    date = st.text_area(label='Choose a maximum date & Ctrl+Enter',
                              value=None, placeholder= 'yyyy-mm-dd\nmin-date = 2020-01-01')
    if date is not None:
        st.write(f'You entered: {date}')
        for i in range(0,len(posts)):
            mask_date_max.append(posts[i]['date'] < date)
    elif politician is None:
        st.write('')
        
        # make a mask with every entry = True
        for i in range(0,len(posts)):
            mask_date_max.append(posts[i]['date'] == posts[i]['date'])
    #elif politician not in list(infos_show['name']):
     #   st.write('You have a typo!')
# ***********************************************************
# Title
st.title('The social politician')

#***** Page 1: Posting Behaviour ************
st.markdown('''
## Posting Behaviour on party level
''')

#***** Page 1: Posting Behaviour ************   1) Show infos_table

# Show Dataframe with Filter
st.write('Infos about followers and posts of politicians:')
st.dataframe(infos_show.loc[mask_parties,['name', 'account', 'party',
                                          'follower_cnt', 'following_cnt', 'post_cnt',]])


# *********************************************************************
#***** Page 1: Posting Behaviour ************   2) Show pie chart & aggregate
# aggregate on party level
aggregate = (
    infos_show[mask_parties]
    .groupby('party')
    .agg(politician_cnt=('party', 'count'),
        mean_follower_cnt=('follower_cnt', lambda x: round(x.mean(),0)),
        mean_post_cnt=('post_cnt', lambda x:  round(x.mean(),0)))
)

# plotting the pie chart
make_pie_2(aggregate,['mean_follower_cnt','mean_post_cnt'],['Average Follower Count','Average Post Count'])
# print the table
st.write('See the table:')
st.dataframe(aggregate)

# *********************************************************************
#***** Page 2: Posting Behaviour ************   1) show posts of politicians


st.title('Posts of Politicians')

show = ['name', 'date', 'likes', 'comments', 'video_views', 'comment', 'webpage'] #,'shortcode'
# write the dataframe according to choosen politicians
df2=pd.DataFrame(columns=show)   # empty df for concatenating
for i in range(0,len(posts)):    # loop all chunks
    df = posts[i].loc[(mask_pol[i])&(mask_date_max[i])]  # write a df with only masked 
    df2=pd.concat([df2, df],axis=0)      # concatenate from all dfs

# show the dataframe with url to click on 
st.data_editor(
    df2,
    column_config={
        'webpage': st.column_config.LinkColumn(
            'Content',
            validate=r'^https?://[^\s]+$',
            display_text='Show Content',  # Display only the domain or customize
            max_chars=50,
        ),
    },
    hide_index=True,
)

#***** Page 2: Posting Behaviour ************   2) show timeline of posts
show_plot = ['name', 'date', 'likes', 'comments', 'video_views', 'comment', 'webpage'] #,'shortcode'
# write the dataframe according to choosen politicians
df3=pd.DataFrame(columns=show)   # empty df for concatenating
for i in range(0,len(posts)):    # loop all chunks
    df = posts[i].loc[(mask_pol[i])&(mask_date_max[i])]  # write a df with only masked 
    df3=pd.concat([df3, df],axis=0)      # concatenate from all dfs

# Chart
what='likes'
timeagg = df3.resample('ME', on='date')[what].sum().reset_index()
st.line_chart(data = df3, x = 'date', y = 'likes')
# *********************************************************************+ Markdown




# Slider
#slider_value = st.slider('Select a number:', 0, 100)
#st.write(f'You selected: {slider_value}')

# Dropdown menu
#dropdown_value = st.selectbox('Choose a party:', ['SPD', 'GRÜNE', 'CSU', 'CDU', 'AfD', 'FDP', 'DIE LINKE', 'SSW'])
#st.write(f'You chose: {dropdown_value}')

# Radio buttons
#radio_button_value = st.radio('Select a language:', ['English', 'Spanish', 'French'])
#st.write(f'You selected: {radio_button_value}')

# Text area
#text = st.text_area('Enter some text:')
#if text:
#    st.write(f'You entered: {text}')

# Button
#if st.button('Click me!'):
#    st.write('You clicked the button!')

# Chart
#data = {'x': [1, 2, 3, 4, 5], 'y': [6, 7, 2, 4, 5]}
#st.line_chart(data)

# Map
#map_data = [
#    {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
#    {'name': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437},
#    {'name': 'Chicago', 'lat': 41.8783, 'lon': -87.6233},
#]
#st.map(map_data)