from sklearn.base import TransformerMixin

class EmptyValuesFilter(TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, df, y=None, **fit_params):
        print("(fit) Empty values filter")
        return self

    def transform(self, df, **transform_params):
        print("(transform) Empty values filter")
        df = df.dropna(subset=self.columns)

        for column in self.columns:
            df = df[df[column] != '']

        return df
