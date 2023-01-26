# followed https://www.kirenz.com/post/2021-12-11-text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/text-mining-and-sentiment-analysis-with-nltk-and-pandas-in-python/


from textblob import TextBlob
import pandas as pd

from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist


import matplotlib.pyplot as plt
from wordcloud import WordCloud

from nltk.sentiment import SentimentIntensityAnalyzer

import seaborn as sns


def jsonToDf(data):
    stopword = stopwords.words("english")

    df = pd.read_json(data)
    df['body'] = df['body'].astype(str).str.lower()



    regexp = RegexpTokenizer('\w+')

    df['text_token']=df['body'].apply(regexp.tokenize)
    df['text_token'] = df['text_token'].apply(lambda x: [item for item in x if item not in stopword])
    df['text_string'] = df['text_token'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))

    all_words = ' '.join([word for word in df['text_string']])
    tokenized_words = word_tokenize(all_words)
    fdist = FreqDist(tokenized_words)
    df['text_string_fdist'] = df['text_token'].apply(lambda x: ' '.join([item for item in x if fdist[item] >= 1 ]))


    wordnet_lem = WordNetLemmatizer()
    df['text_string_lem'] = df['text_string_fdist'].apply(wordnet_lem.lemmatize)
    df['is_equal']= (df['text_string_fdist']==df['text_string_lem'])

    all_words_lem = ' '.join([word for word in df['text_string_lem']])


    wordcloud = WordCloud(width=600, 
                        height=400, 
                        random_state=2, 
                        max_font_size=100).generate(all_words_lem)

    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # print(df.head())
    # plt.show()


    analyzer = SentimentIntensityAnalyzer()
    df['polarity'] = df['text_string_lem'].apply(lambda x: analyzer.polarity_scores(x))

    # Change data structure
    df = pd.concat(
        [df.drop(['polarity'], axis=1), 
        df['polarity'].apply(pd.Series)], axis=1)


    df['sentiment'] = df['compound'].apply(lambda x: 'positive' if x >0 else 'neutral' if x==0 else 'negative')


    return df

