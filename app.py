import streamlit as st
import pymongo
import mysql.connector
import time as t
import pandas as pd
from googleapiclient.discovery import build
APIkey = "AIzaSyCmW6n0O7MHoGKBbGxrH9LJvc0cSUx51Iw"
youtube = build("youtube", "v3", developerKey=APIkey)
from pprint import pprint
st.set_page_config(page_title="Streamlit App", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")
from PIL import Image
logo_path = r"C:\Users\Senthil\Desktop\DS\Projects I & V\youtube.png"
image = Image.open(logo_path)
st.image(image, width=300)
st.header(":red[YOUTUBE DATA HARVESTING AND WAREHOUSEING]")
A = st.selectbox("Select a Channel", ["Select Channel ID","UCwr-evhuzGZgDFrq_1pLt_A", "UCfk1zUguz21peGdIFGKPeVg", "UCUUlw3anBIkbW9W44Y-eURw", "UCuI5XcJYynHa5k_lqDzAgwQ"])
def channel1(A):
    try:
        request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=A
    )
        response = request.execute()
        request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=A,
        maxResults=25
    )
        respons = request.execute()
        channel_1 = dict(Channel_Title= response['items'][0]['snippet']['localized']['title'],
                    #   channel_id = response['items'][0]['id'],
                    #   Channel_Description= response['items'][0]['snippet']['description'],
                      Channel_SubcriberCount = response['items'][0]['statistics']['subscriberCount'],
                      Channel_videoCount= response['items'][0]['statistics']['videoCount'],
                      Channel_viewCount= response['items'][0]['statistics']['viewCount'])
                    #   playlist_id = [respons['items'][0]['id'],respons['items'][1]['id']])
  # channel = "\n".join([f"{key} = {repr(value)}" for key, value in channel_1.items()])

        return channel_1
    except Exception as e:
        st.error(f"Error: {'Invalid Channel ID'}", icon="🚨")
        st.button("Clear")
if A: 
  if A!= "Select Channel ID" :
    if st.button('Fetch'):
      with st.spinner("Just Wiat..."):
        a = channel1(A)
        st.write("You Selected:")
        for key, value in a.items():
          st.write(f"{key} = {repr(value)}")
        st.button('clear') 
 
B = st.text_input("Type Channel ID")

if st.button('Search'):
    if B:
      with st.spinner("Just Wait..."):
        b = channel1(B)
      if b is not None:
        st.write("You Selected:")
        for key, value in b.items():
          st.write(f"{key} = {repr(value)}")
        st.button('clear')
    else:
        st.warning("Please Insert A Valid YouTube Channel ID.")


def get_channel_info(channel_id):
    
    request = youtube.channels().list(
                part = "snippet,contentDetails,Statistics",
                id = channel_id)
            
    response1=request.execute()

    for i in range(0,len(response1["items"])):
        data = dict(
                    Channel_Name = response1["items"][i]["snippet"]["title"],
                    Channel_Id = response1["items"][i]["id"],
                    Subscription_Count= response1["items"][i]["statistics"]["subscriberCount"],
                    Views = response1["items"][i]["statistics"]["viewCount"],
                    Total_Videos = response1["items"][i]["statistics"]["videoCount"],
                    Channel_Description = response1["items"][i]["snippet"]["description"],
                    Playlist_Id = response1["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
                    )
        return data



def get_playlist_info(channel_id):
    All_data = []

    request = youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channel_id,
            maxResults=50,
           
            )
    response = request.execute()

    for item in response['items']: 
            data={'PlaylistId':item['id'],
                    'Title':item['snippet']['title'],
                    'ChannelId':item['snippet']['channelId'],
                    'ChannelName':item['snippet']['channelTitle'],
                    'PublishedAt':item['snippet']['publishedAt'],
                    'VideoCount':item['contentDetails']['itemCount']}
            All_data.append(data)

        
    return All_data
    

def get_channel_videos(channel_id):
    video_ids = []
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    res = youtube.playlistItems().list( 
                                           part = 'snippet',
                                           playlistId = playlist_id, 
                                           maxResults = 30)
    res = res.execute()                                  
                                       
        
    for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
    return video_ids

def get_video_info(video_ids):

    video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id= video_id)
        response = request.execute()

        for item in response["items"]:
            data = dict(Channel_Name = item['snippet']['channelTitle'],
                        Channel_Id = item['snippet']['channelId'],
                        Video_Id = item['id'],
                        Title = item['snippet']['title'],
                        Tags = item['snippet'].get('tags'),
                        Thumbnail = item['snippet']['thumbnails']['default']['url'],
                        Description = item['snippet']['description'],
                        Published_Date = item['snippet']['publishedAt'],
                        Duration = item['contentDetails']['duration'],
                        Views = item['statistics']['viewCount'],
                        Likes = item['statistics'].get('likeCount'),
                        Comments = item['statistics'].get('commentCount'),
                        Favorite_Count = item['statistics']['favoriteCount'],
                        Definition = item['contentDetails']['definition'],
                        Caption_Status = item['contentDetails']['caption']
                        )
            video_data.append(data)
    return video_data

def get_comment_info(video_ids):
        Comment_Information = []
     
        for video_id in video_ids:

                        request = youtube.commentThreads().list(
                                part = "snippet",
                                videoId = video_id,
                                maxResults = 10
                                )
                        response5 = request.execute()
                        
                        for item in response5["items"]:
                                comment_information = dict(
                                        Comment_Id = item["snippet"]["topLevelComment"]["id"],
                                        Video_Id = item["snippet"]["videoId"],
                                        Comment_Text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                                        Comment_Author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                        Comment_Published = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])

                                Comment_Information.append(comment_information)
      
                
        return Comment_Information
def channel_details(channel_id):
    ch_details = get_channel_info(channel_id)
    pl_details = get_playlist_info(channel_id)
    vi_ids = get_channel_videos(channel_id)
    vi_details = get_video_info(vi_ids)
    com_details = get_comment_info(vi_ids)
    conn = pymongo.MongoClient("mongodb://localhost:27017")
    db = conn["YouTube"]
    coll1 = db["channel_details"]
    coll1.insert_one({"channel_information":ch_details,"playlist_information":pl_details,"video_information":vi_details,
                     "comment_information":com_details})
    
    return "upload completed successfully"
col1, col2 = st.columns(2)

if col1.button('Insert Data Into MongoDB'):
    with st.spinner("Please wait..."):
        if A != "Select Channel ID":
            result_A = channel_details(A)
            st.success(result_A)
        # else:
        #     st.warning("Select A valid channels ID for data insertion.")
        if B:
          z = channel1(B)
          if z is not None:
            result_B = channel_details(B)
            st.success(result_B)
        # else:
        #     st.warning(" Entered valid channels ID for data insertion.")
        


#MYSQL

def channel_info():
  v = []
  conn = pymongo.MongoClient("mongodb://localhost:27017")
  db = conn["YouTube"]
  coll1 = db["channel_details"]
  for i in coll1.find({}, {"_id": 0, "channel_information": 1}):
    v.append(i['channel_information'])

  df = pd.DataFrame(v)


  host = "localhost"
  user = "root"
  password = "PrasHantHCHinnapappal19802003"

  connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

  cursor = connection.cursor()

  cursor.execute("create database if not exists You_Tube4")
  cursor.execute('use You_Tube4') 
  drop_query = "DROP TABLE IF EXISTS channels"
  cursor.execute(drop_query)
  create_table = """create table if not exists channel_info(
                    Channel_Id varchar(80) PRIMARY KEY,
                    Channel_Name varchar(100),
                    Subscription_Count bigint,
                    Views bigint,
                    Total_Videos int,
                    Channel_Description TEXT,
                    Playlist_Id varchar(80)
                )"""
  cursor.execute(create_table)

  insert_info = '''
                    INSERT IGNORE INTO channel_info(
                    Channel_Id,
                    Channel_Name,
                    Subscription_Count,
                    Views,
                    Total_Videos,
                    Channel_Description,
                    Playlist_Id
                ) VALUES(%s,%s,%s,%s,%s,%s,%s)
                '''

# Convert DataFrame to list of tuples for executemany
  data_to_insert = df.to_records(index=False).tolist()

# Use executemany to insert multiple rows
  cursor.executemany(insert_info, data_to_insert)

  connection.commit()


def video_info():
  host = "localhost"
  user = "root"
  password = "PrasHantHCHinnapappal19802003"

  connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)
  cursor = connection.cursor()
  cursor.execute('USE you_tube4')
  drop_query = "DROP TABLE IF EXISTS videos"
  cursor.execute(drop_query)
  create_query = '''
    CREATE TABLE IF NOT EXISTS videos (
        Channel_Name varchar(150),
        Channel_Id varchar(100) ,
        Video_Id varchar(40) PRIMARY KEY  , 
        Title TEXT, 
        Tags TEXT,
        Thumbnail varchar(225),
        Description text, 
        Published_Date varchar(50),
        Duration varchar(50), 
        Views INT, 
        Likes INT,
        Comments INT,
        Favorite_Count INT, 
        Definition TEXT, 
        Caption_Status varchar(50)
    )
'''
  cursor.execute(create_query)
  connection.commit()

  vi_list = []
  conn = pymongo.MongoClient("mongodb://localhost:27017")
  db = conn["YouTube"]
  coll1 = db["channel_details"]
  for vi_data in coll1.find({}, {"_id": 0, "video_information": 1}):
    for i in range(len(vi_data["video_information"])):
        vi_list.append(vi_data["video_information"][i])

  df2 = pd.DataFrame(vi_list)

  for index, row in df2.iterrows():
    # Convert potential list values to strings
    row = row.apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    insert_query = '''
        INSERT IGNORE INTO videos (
            Channel_Name,
            Channel_Id,
            Video_Id, 
            Title, 
            Tags,
            Thumbnail,
            Description, 
            Published_Date,
            Duration, 
            Views, 
            Likes,
            Comments,
            Favorite_Count, 
            Definition, 
            Caption_Status 
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    '''

    values = (
        row['Channel_Name'],
        row['Channel_Id'],
        row['Video_Id'],
        row['Title'],
        row['Tags'],
        row['Thumbnail'],
        row['Description'],
        row['Published_Date'],
        row['Duration'],
        row['Views'],
        row['Likes'],
        row['Comments'],
        row['Favorite_Count'],
        row['Definition'],
        row['Caption_Status']
    )

    try:
        cursor.execute(insert_query, values)
        connection.commit()
        print("Inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Failed insert values: {values}")

  cursor.close()
  connection.close()


def com_info():

  conn = pymongo.MongoClient("mongodb://localhost:27017")
  db = conn["YouTube"]
  coll1 = db["channel_details"]
  host = "localhost"
  user = "root"
  password = "PrasHantHCHinnapappal19802003"

  connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

  cursor = connection.cursor()
  cursor.execute('use You_Tube4')
  drop_query = "DROP TABLE IF EXISTS comments"
  cursor.execute(drop_query)
  create_query = '''CREATE TABLE if not exists comments(Comment_Id varchar(100) PRIMARY KEY ,
                       Video_Id varchar(80) ,
                       Comment_Text text, 
                       Comment_Author varchar(150),
                       Comment_Published varchar(50))'''
  cursor.execute(create_query)

  com_list = []
    
  for com_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(com_data["comment_information"])):
            com_list.append(com_data["comment_information"][i])
  df3 = pd.DataFrame(com_list)


  for index, row in df3.iterrows():
            insert_query = '''
                INSERT IGNORE INTO comments (Comment_Id,
                                      Video_Id ,
                                      Comment_Text,
                                      Comment_Author,
                                      Comment_Published)
                VALUES (%s, %s, %s, %s, %s)

            '''
  data_to_insert = df3.to_records(index=False).tolist()           
  cursor.executemany(insert_query, data_to_insert)
  connection.commit()
  cursor.close()
  connection.close()          
 
if col2.button('From MongoDB Data Inserted into Mysql'):
  with st.spinner("Just Wiat"):
    t.sleep(5)
    channel_info()
    video_info()
    com_info()
    st.success('Successfully! From Mongodb Data Inserted Into Mysql!', icon="✅")   




st.header(":red[Analytics!]")

host = "localhost"
user = "root"
password = "PrasHantHCHinnapappal19802003"

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

cursor = connection.cursor()
cursor.execute('USE you_tube')
def Q1():          
  sql_query = "SELECT Title, Channel_Name FROM videos;"
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
# a = cursor.description
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)

  cursor.close()
  connection.close()
if st.button('What are the names of all the videos and their corresponding channels?'):
  Q1()
  st.button('clear')
# a = st.empty()
 
 
def Q2():
  sql_query = """
    SELECT Channel_Name, COUNT(*) AS VideoCount
    FROM videos
    GROUP BY Channel_Name
    ORDER BY VideoCount ASC;
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  for row in result_set:
    channel_name, video_count = row
  st.write(f"Channel Name: {channel_name}, Video Count: {video_count}")
  cursor.close()
  connection.close() 

if st.button('Which channels have the most number of videos, and how many videos do they have?'):
      Q2()
      st.button('clear') 

def Q3():
  sql_query = """
    SELECT Title, Channel_Name, Views
    FROM videos
    ORDER BY Views DESC
    LIMIT 10;
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('What are the top 10 most viewed videos and their respective channels?'):
      Q3()
      st.button('clear') 


def Q4():
  sql_query = """
    SELECT Channel_Name, Title,Comments
    FROM videos;   
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('How many comments were made on each video, and what are theircorresponding video names?'):
      Q4() 
      st.button('clear')


def Q5():
  sql_query = """
    SELECT Channel_Name, Title, Likes
    FROM videos
    ORDER BY Likes DESC
    LIMIT 1;
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('Which videos have the highest number of likes, and what are their corresponding channel names?'):
  Q5()
  st.button('clear') 


def Q6():
  sql_query = """
    SELECT Channel_Name, Title, Likes
    FROM videos;   
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('What is the total number of likes and dislikes for each video, and what are their corresponding video names?'):
      Q6() 
      st.button('clear')


def Q7():
  cursor = connection.cursor()
  cursor.execute('USE you_tube')
  sql_query = """
    SELECT Channel_Name, SUM(Views) AS TotalViews
    FROM videos
    GROUP BY Channel_Name;
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('What is the total number of views for each channel, and what are their corresponding channel names?'):
      Q7() 
      st.button('clear')



def Q8():
  cursor = connection.cursor()
  cursor.execute('USE you_tube')
  sql_query = """
    SELECT DISTINCT Channel_Name
    FROM videos
    WHERE YEAR(Published_Date) = 2023;
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  for t in result_set:
    st.write(t)
  cursor.close()
  connection.close()
if st.button('What are the names of all the channels that have published videos in the year2023?'):
      Q8()
      st.button('clear') 



def Q9():
  sql_query = """
    SELECT
    Channel_Name,
    AVG(
        TIME_TO_SEC(
            IF(POSITION('M' IN Duration) > 0,
                SUBSTRING_INDEX(SUBSTRING_INDEX(Duration, 'M', 1), 'T', -1) * 60,
                0
            )
            +
            IF(POSITION('S' IN Duration) > 0,
                SUBSTRING_INDEX(SUBSTRING_INDEX(Duration, 'S', 1), 'M', -1),
                0
            )
        )
    ) as AverageDuration
  FROM videos
  GROUP BY Channel_Name;"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('What is the average duration of all videos in each channel, and what are their corresponding channel names?'):
  Q9()
  st.button('clear') 



def Q10():
  sql_query = """
    SELECT Channel_Name, MAX(Comments) as MaxComments
    FROM videos
    GROUP BY Channel_Name;
    
"""
  cursor.execute(sql_query)
  result_set = cursor.fetchall()
  a = pd.DataFrame(result_set,columns=[i[0] for i in cursor.description])
  st.write(a)
  cursor.close()
  connection.close()
if st.button('Which videos have the highest number of comments, and what are their corresponding channel names?'):
  Q10() 
  st.button('Clear')  
# st.balloons() 
st.sidebar.title("WELCOME TO YOUTUBE DATA HARVESTING AND WAREHOUSEING PROJECT USING MYSQL,MONGODB AND STREAMLIT")
st.sidebar.title("CHANNEL IDs")
w = ["UCwr-evhuzGZgDFrq_1pLt_A", 'UCfk1zUguz21peGdIFGKPeVg', 'UCUUlw3anBIkbW9W44Y-eURw', 'UCuI5XcJYynHa5k_lqDzAgwQ']
for i in w:
    st.sidebar.write(i)

data = 'Pandas' ,'Mysql', 'Mongodb', 'Streamlit', 'google-api-python-client', 'Python','https://github.com/Prashanth292003/YOUTUBE-DATA-HARVESTING-AND-WAREHOUSEING-PROJECT'
data_string = '\n'.join(data)
st.sidebar.download_button('Download File',data_string , key='file_download' )

if st.sidebar.button("Click to get Github Link"):
  st.sidebar.write("https://github.com/Prashanth292003/YOUTUBE-DATA-HARVESTING-AND-WAREHOUSEING-PROJECT")
  st.sidebar.button("Hide")

#FINISHED






