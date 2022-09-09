from importlib.resources import path


def get_news(search_query):
    from pygooglenews import GoogleNews
    import pandas as pd
    import json

    path ='C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\news_output\\'
################################scrapping
    def get_titles(keyword):
        news= []
        gn=GoogleNews(lang='th',country='TH')
        # search = gn.search(keyword, when = '5d')
        search = gn.search(keyword)
        articles = search['entries']
        for i in articles:
            article = {'หัวเรื่อง': i.title, 'ลิงค์': i.link,"วันที่":i.published}
            news.append(article)
        return news

    data = get_titles(search_query)
    df_all = pd.DataFrame(data)

    ################################ create แหล่งข่าว

    df_all['แหล่งข่าว'] = df_all['หัวเรื่อง'].str.extract('-( .*$)')
    #date sort
    df_all["วันที่"] = pd.to_datetime(df_all["วันที่"])
    df_all.sort_values(by='วันที่', ascending = False, inplace=True)

    #move column
    result_df = df_all[['วันที่','หัวเรื่อง','แหล่งข่าว','ลิงค์']]
    result_df_done = pd.DataFrame(result_df)

    #reset Index

    result_reset = result_df_done.reset_index(drop=True)
    result_reset['วันที่'] = result_reset['วันที่'].dt.strftime('%Y-%m-%d %H:%M:%S')

    result_reset.to_csv(path +'news.csv')

    ################################ count แหล่งข่าว

    a = pd.DataFrame(result_reset['แหล่งข่าว'].value_counts())
    a.to_csv(path +'news_publisher_count.csv')

    a_dict = result_reset.to_dict('records')
    #create Json
    json_object = json.dumps(a_dict, indent = 4) 
    #save to Json file
    with open(path+"news.json", "w", encoding='utf8') as outfile:
        json.dump(a_dict, outfile, indent=4, ensure_ascii=False)

    print('all done')
    return json_object, result_reset
#return json_object, result_reset

a = 'มหาวิทยาลัยขอนแก่น'
get_news(a)