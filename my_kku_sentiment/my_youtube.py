def get_youtube(query_terms) :
    # library googleapiclient installed with: pip install --upgrade google-api-python-client
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import json

    path = 'C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\yt_output\\'
    # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    DEVELOPER_KEY = 'AIzaSyCHXPnp_7yO76B_DUmdBERQhS5daRBILNo'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query_terms,
        part='id,snippet',
        type='video',
        relevanceLanguage='en',
        maxResults=3
    ).execute()
    print(search_response['pageInfo']['totalResults'])

    video_ids = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        video_ids.append(search_result['id']['videoId'])
    print (video_ids)


    # Scrape Comments for SQL Using Python Through The Youtube Data API
    api_key = "AIzaSyCHXPnp_7yO76B_DUmdBERQhS5daRBILNo" # Insert your Api key here.
    #
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=api_key)

    import pandas as pd

    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count', 'publishedAt']]

    def scrape_comments_with_replies():
        data = youtube.commentThreads().list(part='snippet', videoId=id_code, maxResults='100', textFormat="plainText").execute()
        
        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']
            # publishedAt = i["snippet"]['topLevelComment']["snippet"]
            
            box.append([name, comment, published_at, likes, replies])
            
            totalReplyCount = i["snippet"]['totalReplyCount']
            
            if totalReplyCount > 0:
                
                parent = i["snippet"]['topLevelComment']["id"]
                
                data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                            textFormat="plainText").execute()
                
                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ""

                    box.append([name, comment, published_at, likes, replies])

        while ("nextPageToken" in data):
            
            data = youtube.commentThreads().list(part='snippet', videoId=id_code, pageToken=data["nextPageToken"],
                                            maxResults='100', textFormat="plainText").execute()
                                            
            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

                totalReplyCount = i["snippet"]['totalReplyCount']

                if totalReplyCount > 0:
                    
                    parent = i["snippet"]['topLevelComment']["id"]

                    data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                    textFormat="plainText").execute()

                    for i in data2["items"]:
                        name = i["snippet"]["authorDisplayName"]
                        comment = i["snippet"]["textDisplay"]
                        published_at = i["snippet"]['publishedAt']
                        likes = i["snippet"]['likeCount']
                        replies = ''

                        box.append([name, comment, published_at, likes, replies])

        df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                    'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})
        
        sql_vids = pd.DataFrame([])

        sql_vids = sql_vids.append(df, ignore_index = True)

        sql_vids.to_csv(path+'youtube_comments.csv', index=False, header=False)
        return sql_vids

    for id_code in video_ids:
        yt_comment_scrap_df = scrape_comments_with_replies()
        #create dict
        a_dict = yt_comment_scrap_df.to_dict('records')
        #create Json
        json_object = json.dumps(a_dict, indent = 4) 
        #save to Json file
        with open(path+"yt_comment_scrap_dict.json", "w", encoding='utf8') as outfile:
            json.dump(a_dict, outfile, indent=4, ensure_ascii=False)
    print('comment done')

    #######################################title scrap

    def get_video_details(youtube, video_ids):
        import time 
        time.sleep(15)
        all_video_stats = []
        
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                        part='snippet,statistics',
                        id=','.join(video_ids[i:i+50]))
            response = request.execute()
            
            for video in response['items']:
                video_stats = dict(chanelTitle = video['snippet']['channelTitle'],
                                Title = video['snippet']['title'],
                                describe = video['snippet']['description'],
                                Published_date = video['snippet']['publishedAt'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics']['likeCount'],
                                #  Dislikes = video['statistics']['dislikeCount'],
                                Comments = video['statistics']['commentCount']
                                
                                )

                all_video_stats.append(video_stats)
        return all_video_stats

    video_ids = video_ids
    video_details = get_video_details(youtube, video_ids)

    video_data_df = pd.DataFrame(video_details)

    video_data_df['Published_date'] = pd.to_datetime(video_data_df['Published_date']).dt.date
    video_data_df['Views'] = pd.to_numeric(video_data_df['Views'])
    video_data_df['Likes'] = pd.to_numeric(video_data_df['Likes'])
    # video_data_df['Dislikes'] = pd.to_numeric(video_data_df['Dislikes'])
    video_data_df['Views'] = pd.to_numeric(video_data_df['Views'])
    # video_data_df['Describtion'] = pd.to_numeric(video_data_df['Views'])
    video_data_df.to_csv(path + 'youtube_title.csv')

    print('all done')

    return (json_object, video_data_df, yt_comment_scrap_df )
#return (json_object, video_data_df, yt_comment_scrap_df )

query_terms = 'มหาวิทยาลัยขอนแก่น'
get_youtube(query_terms)
