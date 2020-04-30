from sklearn.base import TransformerMixin

class ReplaceOutliersWithPercentile(TransformerMixin):
    def __init__(self, col_names, upper_percentile, lower_percentile):
        self.col_names = col_names
        self.upper_percentile = upper_percentile
        self.lower_percentile = lower_percentile
        self.min_extreme = {}
        self.max_extreme = {}
        self.min_replace = {}
        self.max_replace = {}

    def fit(self, df, y=None, **fit_params):
        print('(fit) Replace outliers for: ',self.col_names, 'with percentiles: (', self.lower_percentile,
              self.upper_percentile, ")")
        for col in self.col_names:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.min_replace[col] = df[col].quantile(self.lower_percentile)
            self.max_replace[col] = df[col].quantile(self.upper_percentile)
            self.min_extreme[col] = (Q1 - 1.5 * IQR)
            self.max_extreme[col] = (Q3 + 1.5 * IQR)
        return self

    def transform(self, df, **transform_params):
        print('(fit) Replace outliers for: ',self.col_names, 'with percentiles: (', self.lower_percentile,
              self.upper_percentile, ")")
        df_copy = df.copy()
        for col in self.col_names:
            extremes_min = df_copy[df_copy[col] < self.min_extreme[col]].index
            extremes_max = df_copy[df_copy[col] > self.max_extreme[col]].index
            df_copy.loc[extremes_min, col] = self.min_replace[col]
            df_copy.loc[extremes_max, col] = self.max_replace[col]
        return df_copy
