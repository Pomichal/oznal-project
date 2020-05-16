from sklearn.base import TransformerMixin, clone

class Scale(TransformerMixin):
    def __init__(self, col_names, scaler):
        self.col_names = col_names
        self.scalers = {}
        for col in col_names:
            self.scalers[col] = clone(scaler)

    def fit(self, df, y=None, **fit_params):
        print("(fit) Scale cols:", self.col_names)
        for col in self.col_names:
            if len(df[col].dropna()) > 0:
                self.scalers[col] = self.scalers[col].fit(df[[col]])
        return self

    def transform(self, df, **transform_params):
        print("(transform) Scale cols:", self.col_names)
        df_copy = df.copy()
        for col in self.col_names:
            df_copy.loc[:, col] = self.scalers[col].transform(df_copy[[col]])
        return df_copy
