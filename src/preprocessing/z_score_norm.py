from sklearn.base import TransformerMixin

class ZScoreNormalization(TransformerMixin):
    def __init__(self, col_names):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) ZScoreNormalization")
        self.mean = {}
        self.std = {}
        for col in self.col_names:
            self.mean[col] = df[col].mean()
            self.std[col] = df[col].std()
        return self

    def transform(self, df, **transform_params):
        print("(transform) ZScoreNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = (df[col] - self.mean[col]) / self.std[col]
            df_copy.loc[:, col] = transformed
        return df_copy
