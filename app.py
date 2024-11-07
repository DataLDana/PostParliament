import streamlit as st
import pandas as pd
import warnings
from functions_app import *
pd.options.display.max_colwidth = None

# ********************************************************************************
# **************  load the files  ***************************************

    
# load variables
# check if already there
if 'posts' not in st.session_state:    # only do if session_state.posts is not there
    
    # load info 
    infos_show = pd.read_csv('Data/infos_show.csv')
    
    infos_show = infos_show.drop('Unnamed: 0', axis = 1)

    ## load election results
    #elections = pd.read_csv('Ergebnisse/election2021.csv')
    #elections = elections.drop('Unnamed: 0', axis = 1)
    
    # load posts
    posts =[]
    i=0
    # load filenames
    FileNames = pd.read_csv("Data/PostFilenames.csv")

    # load post chunks
    for path in FileNames['path']:
        # load the csv
        chunk = change_types(pd.read_csv(path))   # use function to chop datatypes
        # reset index of posts dataframes
        chunk = chunk.set_index('Unnamed: 0')             # get index of original dataframe
        chunk.index.name = None                  # delete the index name
        # append chunk to list of dataframes
        posts.append(chunk)
        i+=1
    
    # load variables into session state    
    st.session_state.posts = posts
    st.session_state.infos = infos_show
    #st.session_state.elections = elections

  



# ********************************************************************************
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
    mask_parties = st.session_state.infos['party'].isin(parties)

    
    # ************choose politician****************
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)
    # selection of a politician
    # Text area
    mask_pol =[]
    politician = st.text_area(label='Choose a politician to be analyzed & Ctrl+Enter',
                              value=None, placeholder= 'Enter one politican here\nType in the name as stated in the tables')
    if politician in list(st.session_state.infos['name']):
        st.write(f'You entered: {politician}')
        for i in range(0,len(st.session_state.posts)):
            mask_pol.append(st.session_state.posts[i]['name'] == politician)
    elif politician is None:
        st.write('')
        # make a mask with every entry = True
        for i in range(0,len(st.session_state.posts)):
            mask_pol.append(st.session_state.posts[i]['name'] == st.session_state.posts[i]['name'])
    elif politician not in list(st.session_state.infos['name']):
        st.write('You have a typo!')

    
    # ************choose a date ****************
    st.markdown("<hr style='border: 1px solid white;'>", unsafe_allow_html=True)

    # Generate a list of month intervals from January 2020 to October 2024
    start, end = st.select_slider(
        'Select a start and end month',
        options=[date.strftime('%Y-%m') for date in pd.date_range(start='2020-01', end='2024-10', freq='MS')],
        value=('2020-01', '2024-10'),
        )
    st.write("You selected month between", start, "and", end)
    
    # Create mask
    mask_date =[]
    for i in range(0,len(st.session_state.posts)):
        mask_date.append((st.session_state.posts[i]['date'] >= start) & (st.session_state.posts[i]['date'] <= end))


# ********************************************************************************   
# ********************** start the app ****************************************
# Title
st.title('PostParliament')
st.markdown('''
The database covers the following information:
* Who?

    All politicians (MPs) of the current german parliament who have an account on instagram
* What?

     **Infos about accounts**
    - The name, the account name and the party of the MP
    - How many followers, and overall posts

     **Infos on posts** 
    - the date
    - how many likes the post got
    - how many comments the post got
    - how many views the video has (if the media type is a reel)
    - what caption the MP wrote
    - a link to the instagram post

* What can you change?
    - which parties to include
    - choose one politician or keep all 
    - select the time span covered

''')

#***** Page 1: Posting Behaviour ************
st.markdown('''
## Followers/Posting on party level
''')

#***** Page 1: Followers/Posts/Comments ************   

# 1) aggregate of posts on politician level -> get aggregate_pol
# 1.1) first create a df according to the filters chosen (party and date)
show = ['name','party', 'likes', 'comments', 'video_views'] # (what cols to show)
df3=pd.DataFrame(columns=show)   # empty df for concatenating

with warnings.catch_warnings():       # supress the warning with pd.concat
    warnings.simplefilter("ignore")
    for i in range(0,len(st.session_state.posts)):    # loop all chunks
        df = st.session_state.posts[i].loc[(st.session_state.posts[i]['party'].isin(parties)) & (mask_date[i])] # write a df with only masked 
        df3=pd.concat([df3, df],axis=0)      # concatenate from all dfs
# 1.2) AGGREGATION OF POSTS on name level
aggregate_pol = (
    df3
    .groupby('name')
    .agg(
        post_cnt=('party', 'count'),
        mean_likes=('likes', lambda x: round(x.mean(),0)),
        mean_comments=('comments', lambda x:  round(x.mean(),0)),
        mean_video_view=('video_views', lambda x:  round(x.mean(),0))
        )
    .reset_index()
)

# 2.) get account information and follower count filtered by party
infos = st.session_state.infos.loc[mask_parties,['name', 'account', 'party',
                                          'follower_cnt']]
# 3.) MERGE info and aggregate_pol
# show post_cnt/likes/comments per party and per person
merge_pol= infos.merge(aggregate_pol, on='name')

#st.write('show info table:')
#st.dataframe(infos)
#st.write('show posts aggregate:')
#st.dataframe(aggregate_pol)

# Show Dataframe 
st.write('Infos about politicians:')
st.dataframe(merge_pol)

# 4.) AGGREGATE OF on party level
aggregate_party = (
    merge_pol
    .groupby('party')
    .agg(politician_cnt=('party', 'count'),
        follower_cnt=('follower_cnt', lambda x: round(x.mean(),0)),
        post_cnt=('post_cnt', lambda x:  round(x.mean(),0)),
        mean_likes=('mean_likes', lambda x: round(x.mean(),0)),
        mean_comments=('mean_comments', lambda x: round(x.mean(),0)),       
        mean_video_view=('mean_video_view', lambda x: round(x.mean(),0))
        )
    .reset_index()
)


st.write('Metrics on party level per MP as pie chart :')
# plotting the pie chart
make_pie_2(aggregate_party,['follower_cnt','post_cnt'],['Percentage of Average Follower per MP per party','Average Posts per MP per party'])
# plotting the pie chart
make_pie_2(aggregate_party,['mean_likes','mean_comments'],['Percentage of Average Likes one MP got for a post','Percentage of Average Comments a MP got for a post'])

st.write('Metrics on party level as table:')
# print the table
st.dataframe(aggregate_party)


# *********************************************************************
#***** Page 2: Posting Behaviour ************   1) show posts of politicians

st.markdown('''
## Posts of MPs
''')
st.write(f'Information on posts of MP {politician} between {start} and {end}')
show = ['name','party', 'date', 'likes', 'comments', 'video_views', 'comment', 'webpage'] #,'shortcode'

# write the dataframe according to choosen politicians
df2=pd.DataFrame(columns=show)   # empty df for concatenating

with warnings.catch_warnings():       # supress the warning with pd.concat
    warnings.simplefilter("ignore")
    for i in range(0,len(st.session_state.posts)):    # loop all chunks
        df = st.session_state.posts[i].loc[(mask_pol[i]) & (mask_date[i])] # write a df with only masked 
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

#***** Page 2: Posting Behaviour ************   2) show time plot
what = st.radio('Select one metric to plot:', ['likes', 'comments',
                                               'video_views', 'All'])
if 'All' in what:
    what = ['likes', 'comments', 'video_views']
    
st.write(f'Average {what} from politician {politician} between {start} and {end}')

timeagg = df2.resample('ME', on='date')[what].mean().reset_index()
st.line_chart(data = timeagg, x = 'date', y = what)

#st.map(map_data)
