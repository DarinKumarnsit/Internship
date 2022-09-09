import pandas as pd

posts = pd.read_csv('C:/Users/ACER/Desktop/kku_sentiment/my_kku_sentiment/ig_output/2get_comment.csv')

# def extract_word1():
#     posts_cm = pd.read_csv('C:/Users/ACER/Desktop/kku_sentiment/my_kku_sentiment/ig_output/3get_comment.csv')
#     return posts_cm

# def extract_word(posts_cm):
#     # posts_cm = pd.read_csv('C:/Users/ACER/Desktop/kku_sentiment/my_kku_sentiment/ig_output/3get_comment.csv')
#     posts_cm2= posts_cm['comment'].str.extract('text=(.+)\suser=(.+)\susername=(.+)\sfull_name=')

#     # print(posts_cm2.columns) 

#     df = posts_cm2.drop(columns=[1])
#     a = df.rename(columns={0:"comment_text", 2: "username"})
#     a.to_csv('4get_comment.csv')

#     return a

# sd = extract_word1()
# s = extract_word(sd)

path='C:\\Users\\ACER\\Desktop\\kku_sentiment\\my_kku_sentiment\\ig_output\\'

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

get_a_column_df = get_comment_to_one_column(posts)
get_comment_final_df = extract_word(get_a_column_df)