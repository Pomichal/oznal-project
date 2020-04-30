from sklearn.base import TransformerMixin

class DropOutliers(TransformerMixin):
    def __init__(self, col_names):
        self.col_names = col_names
        self.min_extreme = {}
        self.max_extreme = {}

    def fit(self, df, y=None, **fit_params):
        print('-- Drop outliers for: ',self.col_names)
        for col in self.col_names:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.min_extreme[col] = (Q1 - 1.5 * IQR)
            self.max_extreme[col] = (Q3 + 1.5 * IQR)
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            extremes_min = df_copy[df_copy[col] < self.min_extreme[col]].index
            extremes_max = df_copy[df_copy[col] > self.max_extreme[col]].index
            df_copy.drop(extremes_min, inplace=True)
            df_copy.drop(extremes_max, inplace=True)
        return df_copy
