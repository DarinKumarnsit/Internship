# #https://github.com/adw0rd/instagrapi

#ดึงโพสกับคอมเม้นที่นี่ Success!!! (8/30)
#put getComment , extractWord here is not work (มากกวา่ 10 ขึ้น  "['index'] not found in axis" line100)

from instagrapi import Client
import json
import pandas as pd
import time

path='C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\ig_output\\'

#login
cl = Client()
USERNAME = 'blackmeowabc'
PASSWORD = '123412345'
cl.login(USERNAME, PASSWORD)

search_query = str(input('Please enter keyword or hashtag to search (without #): '))
hashtag = cl.hashtag_info(search_query)
output = hashtag.media_count
print('media_count =',output)

with open('C:/Users/ACER/Desktop/kku_sentiment/my_kku_sentiment/ig_output/output.json', 'w') as fp:
    json.dump(hashtag.dict(), fp)

print('\n' + 'post list' + '\n')

like_list = []
caption_list = []
date_list = []
comment_count_list = []
userName_list = []
postid_list = []

#rate limit 200 request/hr !!! (30 is ok)
#40 ---> instagrapi.exceptions.ClientConnectionError: ConnectionError ('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))
amount_media = 30
medias = cl.hashtag_medias_recent(search_query, amount=amount_media) 
# medias[n] คือดึงข้อมูล recent จากโพสลำดับที่ n มา #ไม่ใช่ดึงมา n โพสนะ


for i in range(amount_media) :
    # dictOutput = medias[i].dict
    # print(dictOutput)
    print(len(like_list))
    LikeOutput = medias[i].like_count
    textOutput = medias[i].caption_text
    dateOutput = medias[i].taken_at
    commentCountOutput = medias[i].comment_count
    userNameOutput = medias[i].user.username
    idPostOutput = medias[i].id
    time.sleep(3)

    #dict to list
    like_list.append(LikeOutput)
    caption_list.append(textOutput)
    date_list.append(dateOutput)
    comment_count_list.append(commentCountOutput)
    userName_list.append(userNameOutput)
    postid_list.append(idPostOutput)
        
final_result_all_df = pd.DataFrame(list(zip(postid_list,date_list,userName_list, caption_list, comment_count_list, like_list )),columns =['id','date','username','caption', 'comment_count','like'])
final_result_all_df.to_csv(path + '1get_post.csv')
print('post done')

#request comment by id post
#create id_df that have comment
a_df = final_result_all_df[final_result_all_df['comment_count'] != 0]
postId_list = a_df['id'].values.tolist()

comment_list = []
for i2 in range(len(postId_list)):
    a = cl.media_comments(media_id=postId_list[i2]) 
    comment_list.append(a)
    comment_result_df = pd.DataFrame(comment_list)
    comment_result_df.to_csv(path + '2get_comment.csv')
    
print('comment done')

def get_comment_to_one_column(comment_result_df):
    column_list = list(comment_result_df.columns) 

    #make it to one column
    c = pd.melt(comment_result_df, value_vars=column_list, value_name='comment')
    #drop NaN
    c2 = c.dropna()
    c3 = c2.reset_index()
    c3.to_csv(path + '3get_comment.csv')
    return c3

def extract_word(get_a_column_df):
    posts_cm2= get_a_column_df['comment'].str.extract('text=(.+)\suser=(.+)\susername=(.+)\sfull_name=')

    df = posts_cm2.drop(columns=[1])
    df2 = df.rename(columns={0:"comment_text", 2: "username"})
    df2.to_csv(path +  '4get_comment.csv')
    return df2

posts = pd.read_csv('C:/Users/ACER/Desktop/kku_sentiment/my_kku_sentiment/ig_output/2get_comment.csv')

get_a_column_df = get_comment_to_one_column(posts)
get_comment_final_df = extract_word(get_a_column_df)


# #7.54
# #8.37
# #9.05-9.13(no wifi)
# #11.30
# #11.52
# #12.10
# #12.30
# #12.55-1.20

# #######

# #2.51
# #3.31-3.41 (30post)

# #######
# #3.33 connect error try change proxy (50 media)
# #3.55 
# #4.12-4.21
# #4.38-4.44
# #4.52
# #6.19-6.30
# #6.45-6.52 (scrap เร็ว)
# #7.07
# #7.23-7.28
#7.43-7.51
#11.43
#12.05
#12.34
#12.50
#####################
#6.20-6.25
#############
#10.39 TypeError: can only concatenate str (not "int") to str ###but i type str 
#10.50 everything's fine (30)
#commenrresult_df not define line79
##############
#12.35 
#1225ClientNotFoundError: 404 Client Error for challenge
#1234
#1235 ได้เฉย
#1.06
#1.17
#2.31