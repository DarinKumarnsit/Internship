#error
#requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))
#https://github.com/RallyTools/RallyRestToolkitForPython/issues/179  วิธีแก้คือรอ 10 นาที

#getpost and comment

import time
from facebook_scraper import *
import pandas as pd
from requests.exceptions import TooManyRedirects

path='C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\fb_output\\'

search_query = str(input('Please enter keyword or hashtag to search (without #): '))
results = []
reaction_list=[]
start_url = None
def handle_pagination_url(url):
    global start_url
    start_url = url
set_cookies("facebook.com_cookies.txt")


def get_comment(posts_id, start_url) : 

    def handle_pagination_url(url):
        global start_url
        start_url = url
    
    have_comments_df = posts_id[posts_id['comments'] != 0]
    #filter id post (get only int id)
    have_comments_df2 = have_comments_df[posts_id['post_id'].astype(str).str.isdigit()]
    have_comments_df2.to_csv(path + 'idPost_df.csv')
    #id_df to list
    postsId_list = have_comments_df2['post_id'].values.tolist()
    print(postsId_list)

    comment_results = []
    for i in range(len(postsId_list)):
        print('post no.', i+1)
        post = next(
            get_posts(
                #แยก df ที่มี idpost ออกมา แล้ว for loop
                post_urls=[postsId_list[i]],
                options={
                    "comments": "generator",
                    "comment_start_url": start_url,
                    "comment_request_url_callback": handle_pagination_url,
                },
            )
        )
        
        comments = post["comments_full"]

        for comment in comments:
            print('comment no.', len(comment_results))
            # print(comment)
            comment_results.append(comment)
            comment_resultdf = pd.DataFrame(comment_results)
            comment_resultdf.to_csv(path + 'getComment.csv')

        print("comment done", '\n')
        time.sleep(5)

    print("comment all done", '\n')  
    return comment_resultdf

while True:
    try:
        for post in get_posts(hashtag= search_query, page_limit=None, start_url=start_url, request_url_callback=handle_pagination_url, 
                            options={"comments": "generator",
                                    "reactions": True, 
                                    "HQ_images": False, 
                                    "reactors": False,
                                    "allow_extra_requests": False
                                 }):
            print(len(results))
            results.append(post)
            final_result = pd.DataFrame(results)
            #if post dont have reaction its still get reaction
            if post['reactions']: 
                reaction_list.append(post['reactions'])
            reaction_result = pd.DataFrame(reaction_list)

            final_result_all = final_result.join(reaction_result)
            final_result_all.to_csv(path + 'getPost.csv')

        print("post done")

        break
        
    #got error ---> wait 10 min
    except exceptions.TemporarilyBanned:
        print("Temporarily banned, sleeping for 10m")
        time.sleep(600)
    
    except TooManyRedirects:
        print("(TooManyRedirects)Scrapping comment in 2m")
        time.sleep(120)
        get_comment(final_result_all, start_url)
        print("comment done")
        break

    except IndexError:
        print("(IndexError)Scrapping comment in 2m")
        time.sleep(120)
        get_comment(final_result_all, start_url)
        print("comment done")
        break



#1:52 can scrap 20 post then got error index
#11.58
#12.54

#6.45
#8.20 requests.exceptions.TooManyRedirects: Exceeded 30 redirects. (เพิ่งเคยรันแบบใส่ keyword)

#10.36 get only 4 post (มข)
#10.46 get 13 post (kku) requests.exceptions.TooManyRedirects: Exceeded 30 redirects.
#11.01 change cookie (still TooManyRedirects when 13)
#11.25 (kku) An existing connection was forcibly closed by the remote host (got 17)
#11.41 (use comment def) get 20 post then requests.exceptions.TooManyRedirects: Exceeded 30 redirects.
#12.08 import TooManyRedirects (got 18 and  list index out of range) 
#12.39 it's work!!! ignore exeption and go scrap comment !(17)
#1.05 (add start url to comment def)
#1.20 yippyy!! all work
###########
#12.07 got 23 then index error
###########
#10.18 got 36**** then (TooManyRedirects)..
#########
#12.54 got 32 then (TooManyRedirects)..