
def get_tiktok(search_query):
    from TikTokApi import TikTokApi
    import pandas as pd
    import json

    path = 'C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\tt_output\\'
    # search_query = str(input('Please enter keyword or hashtag to search (without #): '))

    with TikTokApi(use_api_endpoints=True) as api:
        tag = api.hashtag(name=search_query)
        print(tag.info())
        result_list = []
        result_stat_list = []
        result_author_list = []
        for video in tag.videos(1):  
            print(len(result_list))      
            result = video.as_dict
            result_stat = video.stats
            result_user = video.author.username

            result_list.append(result)
            result_stat_list.append(result_stat)
            result_author_list.append(result_user)

        #comment scrape 
        def get_comment(tag):

            comment_list = []
            for video in tag.videos(1):        
                for comment in video.comments(1):
                    print(len(comment_list))      
                    tiktok_comment = comment.as_dict
                    comment_list.append(tiktok_comment)

            df = pd.DataFrame(comment_list)     
            df.to_csv(path+'tt_get_comment.csv')
            print('comment done')
            return df

        comment_df = get_comment(tag)
        print('comment column',comment_df.columns)

        

    df = pd.DataFrame(result_list) 
    df2 = pd.DataFrame(result_stat_list)  
    df3 = pd.DataFrame(result_author_list, columns=['username'])
    df3.to_csv(path +'tt_post_author.csv')

    rap = df.join(df2)
    all_rap = rap.join(df3)
    all_rap.to_csv(path+'tt_get_post.csv')

    print('post done')

    ###############time convert 
    #for post
    all_rap['createTime'] = pd.to_datetime(all_rap['createTime'],unit='s')

    df_post = pd.DataFrame(all_rap) 
    #get wanted data column from post 
    df_post2 = df_post.loc[:, ["username","createTime","desc", 'commentCount', 'diggCount', 'playCount', 'shareCount']]
    df_post2['createTime'] = df_post2['createTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_post2.to_csv(path +'tt_post_time_convert.csv')

    #create dict
    a_dict = df_post2.to_dict('records')
    json_object = json.dumps(a_dict, indent = 4) 
    with open("tt_post_time_convert.json", "w", encoding='utf8') as outfile:
        json.dump(a_dict, outfile, indent=4, ensure_ascii=False)

    print('tt_post_time_convert done')

    #for comment (create_time)
    comment_df.rename(columns = {'digg_count':'comment_likes'}, inplace = True)
    comment_df['create_time'] = pd.to_datetime(comment_df['create_time'],unit='s')
    comment_df['create_time'] = comment_df['create_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    comment_df2 = comment_df.loc[:, ["cid","create_time","text", 'comment_likes']]

    df_comment = pd.DataFrame(comment_df2)  

    #create dict
    a_comment_dict = df_comment.to_dict('records')
    json_object = json.dumps(a_comment_dict, indent = 4) 
    with open(path+"tt_comment_time_convert.json", "w", encoding='utf8') as outfile:
        json.dump(a_comment_dict, outfile, indent=4, ensure_ascii=False)

    df_comment.to_csv(path +'tt_comment_time_convert.csv')
    print('tt_comment_time_convert all done')

    return json_object,df_post2, df_comment
    
#return json_object,df_post2, df_comment
a = 'kku'
get_tiktok(a)