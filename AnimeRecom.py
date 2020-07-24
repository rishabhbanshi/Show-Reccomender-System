import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import random as random
from jikanpy import Jikan
import time


jikan=Jikan()


def get_title_from_index(anime_id):
    return df[df.anime_id == anime_id]["name"].values[0]


def get_index_from_name(name):
    return df[df.name == name]["anime_id"].values[0]

# Reading dataset
df=pd.read_csv("anime.csv")


# DATA PRE-PROCESSING
# Handling missing rating
df.loc[df['rating'].isnull(),'rating']=0.0


missing=df.loc[(df['episodes']=="Unknown") & (df['type'].isnull())].copy()

df.loc[(df['name'] == "Steins;Gate 0"), 'type'] = 'TV'
df.loc[(df['name'] == "Steins;Gate 0"), 'episodes'] = '23'
df.loc[(df['name'] == "Violet Evergarden"), 'type'] = 'TV'
df.loc[(df['name'] == "Violet Evergarden"), 'episodes'] = '13'
df.loc[(df['name'] == "Code Geass: Fukkatsu no Lelouch"), 'type'] = 'TV'
df.loc[(df['name'] == "Code Geass: Fukkatsu no Lelouch"), 'episodes'] = '25'
df.loc[(df['name'] == "K: Seven Stories"), 'type'] = 'Movie'
df.loc[(df['name'] == "K: Seven Stories"), 'episodes'] = '6'
df.loc[(df['name'] == "Free! (Shinsaku)"), 'type'] = 'TV'
df.loc[(df['name'] == "Free! (Shinsaku)"), 'episodes'] = '12'
df.loc[(df['name'] == "Busou Shoujo Machiavellianism"), 'type'] = 'TV'
df.loc[(df['name'] == "Busou Shoujo Machiavellianism"), 'episodes'] = '12'
df.loc[(df['name'] == "Code:Realize: Sousei no Himegimi"), 'type'] = 'TV'
df.loc[(df['name'] == "Code:Realize: Sousei no Himegimi"), 'episodes'] = '12'
df.loc[(df['name'] == "Gamers!"), 'type'] = 'TV'
df.loc[(df['name'] == "Gamers!"), 'episodes'] = '12'
df.loc[(df['name'] == "Ganko-chan"), 'type'] = 'TV'
df.loc[(df['name'] == "Ganko-chan"), 'episodes'] = '10'
df.loc[(df['name'] == "Ginga Eiyuu Densetsu (2017)"), 'type'] = 'OVA'
df.loc[(df['name'] == "Ginga Eiyuu Densetsu (2017)"), 'episodes'] = '110'
df.loc[(df['name'] == "Grancrest Senki"), 'type'] = 'TV'
df.loc[(df['name'] == "Grancrest Senki"), 'episodes'] = '24'
df.loc[(df['name'] == "IDOLiSH7"), 'type'] = 'TV'
df.loc[(df['name'] == "IDOLiSH7"), 'episodes'] = '17'
df.loc[(df['name'] == "Isekai Shokudou"), 'type'] = 'TV'
df.loc[(df['name'] == "Isekai Shokudou"), 'episodes'] = '12'
df.loc[(df['name'] == "Oushitsu Kyoushi Haine"), 'type'] = 'TV'
df.loc[(df['name'] == "Oushitsu Kyoushi Haine"), 'episodes'] = '12'
df.loc[(df['name'] == "Peace Maker Kurogane (Shinsaku)"), 'type'] = 'TV'
df.loc[(df['name'] == "Peace Maker Kurogane (Shinsaku)"), 'episodes'] = '24'
df.loc[(df['name'] == "Seikaisuru Kado"), 'type'] = 'TV'
df.loc[(df['name'] == "Seikaisuru Kado"), 'episodes'] = '12'
df.loc[(df['name'] == "UQ Holder!"), 'type'] = 'TV'
df.loc[(df['name'] == "UQ Holder!"), 'episodes'] = '12'
df.loc[(df['name'] == "Citrus"), 'type'] = 'TV'
df.loc[(df['name'] == "Citrus"), 'episodes'] = '12'
df.loc[(df['name'] == "Hitorijime My Hero"), 'type'] = 'TV'
df.loc[(df['name'] == "Hitorijime My Hero"), 'episodes'] = '12'
# print(missing.shape)

df.dropna(subset=['type'],inplace=True)
# print(df.shape)
# exit(0)


# Handling Genre
df.dropna(subset=['genre'],inplace=True)


# MAIN FUNC
m=df.members.quantile(0.75)
C=df.rating.mean()



# Calculate Weighted Rating
def weighted_raing(df,m,C):
    term=df['members'] /(m+df['members'])
    return  df['rating']*term+(1-term)*C



df['comm_rating']=df.apply(weighted_raing,axis=1,args=(m,C))
# print(df.head())

df.drop(['anime_id','rating','members','episodes'],axis=1,inplace=True)
# print(df.head())

df=pd.concat([df,df['type'].str.get_dummies(),df['genre'].str.get_dummies(sep=',')],axis=1)
# print(df.head())

ani_features=df.loc[:, "Movie":].copy()
# print(ani_features.head())

cosine_sim=cosine_similarity(ani_features.values,ani_features.values)
# print(cosine_sim.shape)

ani_index=pd.Series(df.index,index=df.name).drop_duplicates()





def get_recommendation(anime_name, similarity=cosine_sim):
    idx=ani_index[anime_name]
    print(idx)
    sim_scores=list(enumerate(cosine_sim[idx]))
    sim_scores=sorted(sim_scores,key=lambda x:x[1],reverse=True)
    sim_scores=sim_scores[0:11]
    ani_indices=[i[0] for i in sim_scores]
    result = df[['name']].iloc[ani_indices]

    for data in result.index :
        try:
            time.sleep(4)
            search=jikan.search('anime',result['name'][data])
            result="Info of anime: " + search['results'][0]['title']
            print(result)


        except Exception as e:
            print(e)

get_recommendation('Naruto')




# def randomize():
#                     ele = 12227
#                     i=0
#                     for i in range(5):
#                                         rnd = random.randint(0, ele)
#                                         ani_user=df.iloc[rnd,0]
#                                         i=i+1

# def reccom():
#     try:
#         x1 = entry1.get()
#         print("this is "+ x1)
#         get_recommendation(x1)
#     except Exception as e:
#         print(e)

# def passit():
#             try:
#                 get_recommendation(x1)
#             except Exception as e:
#                 print(e)
#                 ele = 12227
#                 rnd = random.randint(0, ele)
#                 ani_user = df.iloc[rnd, 0]
#                 get_recommendation(ani_user)

