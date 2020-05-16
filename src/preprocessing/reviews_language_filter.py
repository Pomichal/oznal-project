from sklearn.base import TransformerMixin
from langdetect import detect

class ReviewsLanguageFilter(TransformerMixin):
    def __init__(self, column, language):
        self.column = column
        self.language = language

    def fit(self, df, y=None, **fit_params):
        print("(fit) Reviews language filter")
        return self

    def transform(self, df, **transform_params):
        def detect_text(text):
            try:
                return detect(text)
            except:
                return 'unknown'
        print("(transform) Reviews language filter")
        df_copy = df.copy()

        df_copy['lang'] = df_copy[self.column].apply(
            detect_text
        )
        df_copy = df_copy[df_copy.lang == self.language]

        df_copy.drop(['lang'], axis=1, inplace=True)

        return df_copy
