from sklearn.base import TransformerMixin

class DropValues(TransformerMixin):
    def __init__(self, col_names, filter_func):
        self.col_names = col_names
        self.func = filter_func

    def fit(self, df, y=None, **fit_params):
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            df_copy = df_copy[self.func(df_copy, col)]
        return df_copy
