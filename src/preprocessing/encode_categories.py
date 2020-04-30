from sklearn.base import TransformerMixin

class EncodeCategories(TransformerMixin):
    def __init__(self, encoder):
        self.encoder = encoder

    def fit(self, df, y=None):
        print("(fit) Category encoder " + str(self.encoder))
        self.encoder.fit(df)
        return self

    def transform(self, df):
        print("(transform) Category encoder " + str(self.encoder))
        df_copy = df.copy()
        df_copy = self.encoder.transform(df)
        return df_copy
