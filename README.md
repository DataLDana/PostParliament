# PostParliament
The final project of my WBS Coding School Data Science Bootcamp is the web app 'PostParliament'.
I created a database containing information about the Instagram posts of members of the German 
Bundestag via API calls. With the web app (coded with the Python library Streamlit) the user 
can interactively study the MP's posting behavior.

https://postparliament.streamlit.app/

# Database Creation
The creation of the database is shown in the Database folder. Note, that for explanation purposes
only some politicians (not the whole database) are shown to avoid large files in the notebook.
FILES: **election.ipynb**, **GetAccounts.ipynb**, **InstaAPI.ipynb**
RESULTS: **elections**, **accounts_final**, **infos_final**, **posts_all**, 
         **post_show**, **post_chunks(i)**

1) The file **election.ipynb** uses information about the 2021 German Bundestag election
   to identify the names of elected politicians. Additionally, information about the election
   results is added, which can be used later to connect posting behavior and election success.
2) The file **GetAccounts.ipynb** identifies the Instagram accounts using the names from the election
   section and the search name endpoint of the Instagram-scraper-api2 API from rapidapi.com.
   - The result of this step is the file **accounts_final.csv**, which contains the names,
   the Instagram account names, and the Instagram ID of the politicians.
   - Note: there are multiple entries according to the account name found by the API, the right
    accounts cannot be distinguished from faulty ones yet.
3) The file **InstaAPI.ipynb** uses the instagram-bulk-scraper-latest API from rapidapi.com and<br>
     3.1)<br>
   - gets the account info with the 'webget_user_id' endpoint including:
     number of followers, number of posts, instagram bio, and a category (the user can
     specify like 'Politician' or 'Actor')
   - identifies the true political accounts from the faulty ones by applying masks with buzzwords
   - The result of this step is the file **infos_final.csv**<br>
   3.2)<br>
   - pulls the information about posts using the endpoint 'webuser-posts' including
     the instagram 'shortcode', the date of the post, the media type, the number of likes, the number
     of comments, how many views a reel got, the author's caption, and the URL.
     - The resulting variable is **posts_all.csv**<br>
   3.3)<br>
   - some postprocessing/cleaning steps
   - to optimize the performance problems due to large data frames the datatypes are changed
   - posts_all is cleaned to be shown in the app **posts_show.csv**, including the creation
     of the Instagram URL
   - the posts are split into smaller data frames with only 30000 rows, as this is supposed
     to improve the performance of the web application **post_chunks{i}.csv**

# The web application
The web application is made in Python code using the library Streamlit, which turns Python code into 
web apps without the need of front-end experience. Steamlit uses the code saved in GitHub and 
automatically deploys the app. The file **app.py** in the main folder is the main file for the app.
**functions_app.py** defines functions and  **requirements.txt** the requirements for the app. The app.py
loads the database, which is given in the folder Data. Note, that the .streamlit folder is 
necessary to allow files >200mb in the Streamlit app. 

# Planned Updates
Unfortunately, due to the large file database, the app breaks down sometimes, although the performance
improved due to the steps taken. The next update includes:
- further troubleshooting with the large database
- further analysis: comparing election results to posting behavior
- adding sentiment APIS: analyzing the tone of posts and see if certain posts are more successful
