def get_twitter(search_query) :
    import tweepy
    import pandas as pd
    import datetime
    import json

    path =  'C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\twitter_output\\'
    # Authentication
    consumerKey = 'XNOIuee6dGYdCHe6qNyfFPnEe'
    consumerSecret = 'avJBOpqnlWJJlxsNF1nOy6Tkjh0e59rDMLyUAlhzzKMVV1zWmO'
    accessToken = '1548864954152808448-WhHvOYl6JFeiuhKeS7COj0TBxN6Agn'
    accessTokenSecret = 'n84g7KBgO4viBwuq72NQiEy1Q7cMd7NzwFhjpxegMlunm'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(auth)

    #scrapping
    #200 request/hrs
    # search_query = input('Please enter keyword or hashtag to search: ')
    # noOfTweet = int(input ('Please enter how many tweets to analyze: '))

    # get tweets from the API
    tweets = tweepy.Cursor(api.search_tweets,
                q=search_query,
                lang="th",
                # until = ("2022-08-29") #key 28/08 result = 27/08
                ).items(50)

    # store the API responses in a list
    tweets_copy = []
    for tweet in tweets:
        tweets_copy.append(tweet)
        
    print("Total Tweets fetched:", len(tweets_copy))

    # intialize the dataframe
    tweets_df = pd.DataFrame()

    # populate the dataframe
    for tweet in tweets_copy:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_df = pd.concat([tweets_df, pd.DataFrame.from_records([{'user_name': tweet.user.name, 
                                                'user_location': tweet.user.location,
                                                'user_description': tweet.user.description,
                                                'user_verified': tweet.user.verified,
                                                'date': tweet.created_at,
                                                'text': text, 
                                                'hashtags': [hashtags if hashtags else None],
                                                'favorite' : tweet.favorite_count, 
                                                'retweet_count' :tweet.retweet_count
                                                    }])])

    #reply_count is a a part of the premium API
    # retweets count is not a property associated to the Users.
    # show the dataframe
    tweets_df.to_csv(path +'TwitterBeforeDup.csv')

    #remove duplicate tweets (Retweet)
    # tweetDelDup_df = tweets_df.drop_duplicates("text").sort_values(by=['retweet_count'], ascending=False)[['text','retweet_count']]
    tweetDelDup_df = tweets_df.drop_duplicates("text").sort_values(by=['retweet_count'], ascending=False)[['user_name', 'date', 'text', 'hashtags', 'favorite', 'retweet_count']]
    tweetDelDup_df2 = tweetDelDup_df.reset_index()
    tweetDelDup_df3=tweetDelDup_df2.drop(columns=['index'])
    tweetDelDup_df3.to_csv(path +'TwitterAfterDup.csv')

    df = tweets_df.reset_index()
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df2=df.drop(columns=['index', 'user_verified', 'user_location', 'user_description' ])
    df2.to_csv(path +'TwitterFinal.csv')
    print('all done')

    #create dict
    a_dict = df2.to_dict('records')
    #create Json
    json_object = json.dumps(a_dict, indent = 4) 
    #save to Json file
    with open(path+"TwitterFinal.json", "w", encoding='utf8') as outfile:
        json.dump(a_dict, outfile, indent=4, ensure_ascii=False)

    print('comment done')
    return json_object, df2
#return json_object, df2

a = 'มข'
get_twitter(a)