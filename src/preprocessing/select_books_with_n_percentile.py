from sklearn.base import TransformerMixin

class SelectBooksWithNPercentile(TransformerMixin):
    def __init__(self, col_name, lower_percentile):
        self.col_name = col_name
        self.percentile = lower_percentile
        self.bound = 0

    def fit(self, df, y=None):
        self.bound = df[self.col_name].quantile(self.percentile)
        print("(fit) Select books with: " + self.col_name + " >= " + str(self.bound))
        return self

    def transform(self, df):
        print("(transform) Select books with: " + self.col_name + " >= " + str(self.bound))
        return df[df[self.col_name] >= self.bound]
