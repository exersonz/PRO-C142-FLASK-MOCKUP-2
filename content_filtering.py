from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

df = pd.read_csv('articles.csv')
df = df[df['soup'].notna()]
#count the number of words for english
count = CountVectorizer(stop_words = 'english')
#converting it into metrix form
count_matrix = count.fit_transform(df['title'])
#finding similarities
cosine_sim = cosine_similarity(count_matrix, count_matrix)
#resetting the index for our data
df = df.reset_index()
#changing the index to the contentId of the article
indices = pd.Series(df.index, index = df['contentId'])

#creating a function that will get recommendations for us using our cosine_similarity classifier that was created earlier
def get_recommendations(contentId, cosine_sim):
    #finding the index of the article in our dataframe using indices var we created earlier (it contains the index of all articles in the dataframe)
    idx = indices[contentId]
    #creating a list of all the scores of the articles
    sim_scores = list(enumerate(cosine_sim[idx]))
    #using sort() on our data to sort the scores of all the articles and reversing its order
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    #taking elements from 1 to 11
    sim_scores = sim_scores[1:11]
    #taking out the indexes of all the articles that we want to recommend and finally returning the contentIds of all the articles that our system recommends
    article_indices = [i[0] for i in sim_scores]
    return df['contentId'].iloc[article_indices]