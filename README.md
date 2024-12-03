# PostParliament
The final project of my WBS Coding School Data Science Bootcamp is the web app 'PostParliament'.
I created a database containing information about the Instagram posts of members of the German 
Bundestag via API calls. With the web app (coded with the Python library Streamlit) the user 
can study the MP's posting behavior interactively.

https://postparliament.streamlit.app/

# Database Creation
FILES: **election.ipynb**, **GetAccounts.ipynb**, **InstaAPI.ipynb**
RESULTS: **accounts_final.csv**, **infos_final**
The creation of the database is shown in the Database folder. 
1) The file **election.ipynb** uses information about the 2021 German Bundestag election
   to identify the names of elected politicians. Additionally, information about the election
   results is added, which can be used later to connect posting behavior and election success.
2) The file **GetAccounts.ipynb** identifies the Instagram accounts using the names from the election
   section and the search name endpoint of the Instagram-scraper-api2 API from rapidapi.com.
   - The result of this step is the file **accounts_final.csv**, which contains the names,
   the Instagram account names, and the Instagram ID of the politicians.
   - Note: there are double entries according to the account name, the official accounts cannot
   be distinguished yet.
3) The file **InstaAPI.ipynb** uses the instagram-bulk-scraper-latest API from rapidapi.com and
   3.1)
   - gets the account info with the 'webget_user_id' endpoint including:
     number of followers, number of posts, instagram bio, and a category (the user can
     specify like 'Politician' or 'Actor')
   - identifies the true political accounts from the faulty ones by applying masks with buzzwords
   - The result of this step is the file **infos_final.csv**
   3.2)
   - pulls the information about posts using the endpoint 'webuser-posts' including
     the instagram 'shortcode', the date of the post, the media type, the number of likes, the number
     of comments, how many views a reel got, the author's caption and the url.
     - The resulting variable is **posts.csv**
