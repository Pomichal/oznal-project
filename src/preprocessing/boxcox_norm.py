from sklearn.base import TransformerMixin
from scipy.stats import boxcox

class BoxCoxNormalization(TransformerMixin):
    def __init__(self, col_names, new_name=""):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) BoxCoxNormalization")
        self.boxcox_attr = {}
        for col in self.col_names:
            _, self.boxcox_attr[col] = boxcox(df[col])
        return self

    def transform(self, df, **transform_params):
        print("(transform) BoxCoxNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = boxcox(df_copy[col], lmbda=self.boxcox_attr[col])
            df_copy.loc[:,col] = transformed
        return df_copy
