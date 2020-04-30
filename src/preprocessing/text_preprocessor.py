import re
from sklearn.base import TransformerMixin

class TextPreprocessor(TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, df, y=None, **fit_params):
        print("(fit) Text preprocessing")
        return self

    def transform(self, df, **transform_params):
        print("(transform) Text preprocessing")
        df_copy = df.copy()

        # Lowercase text
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: text.lower()
        )
        # Remove special characters
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: re.sub(r'[^a-zA-Z0-9\.,?!]+', ' ', text)
        )
        # Remove urls
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: re.sub(r'(www|http:|https:)+[^\s]+[\w]', '', text)
        )

        return df_copy
