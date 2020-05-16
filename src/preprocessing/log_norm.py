import math
from sklearn.base import TransformerMixin

class LogNormalization(TransformerMixin):
    def __init__(self, col_names, new_name=""):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) LogNormalization")
        return self

    def transform(self, df, **transform_params):
        print("(transform) LogNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = df[col].apply(math.log)
            df_copy.loc[:,col] = transformed
        return df_copy
