from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.pipeline import TransformerMixin
import pandas as pd
import numpy as np
import nltk
from nltk import tokenize

class ExtractSentiment(TransformerMixin):

    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()
        nltk.download('punkt')

    def fit(self, df, y=None):
        print("(fit) ExtractSentiment")
        return self

    def transform(self, df):
        print("(transform) ExtractSentiment")
        sentiment_df = pd.DataFrame(df['review_text'].apply(self.get_sentiment).to_list(),
                                    columns=['neg', 'neu', 'pos', 'compound'],
                                   index = df.index)
        return df.join(sentiment_df)

    def get_sentiment(self, text):
        sentences = []
        sentences_list = tokenize.sent_tokenize(text)
        sentences.extend(sentences_list)
        count = (len(sentences))
        sent = np.array([.0, .0, .0, .0])
        for sentence in sentences:
            scores = self.analyser.polarity_scores(sentence)
            sent += np.fromiter(scores.values(), dtype=float)
        average = sent / count
        return average
