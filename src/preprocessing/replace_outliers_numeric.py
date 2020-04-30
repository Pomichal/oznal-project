from sklearn.base import TransformerMixin

class ReplaceNansNumeric(TransformerMixin):
    def __init__(self, col_names, func_type = 'median'):
        self.col_names = col_names
        self.func_type = func_type

    def fit(self, df, y=None, **fit_params):
        self.na_replace = {}
        for col in self.col_names:
            if(self.func_type == 'median'):
                self.na_replace[col] = df[col].median()
            else:
                self.na_replace[col] = df[col].mean()
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            df_copy.loc[:, col] = df_copy[col].fillna(self.na_replace[col])
        return df_copy

