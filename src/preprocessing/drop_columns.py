from sklearn.base import TransformerMixin

class DropColumns(TransformerMixin):
    def __init__(self, cols):
        self.cols = cols

    def fit(self, df, y=None):
        print("(fit) Drop columns: " + str(self.cols))
        return self

    def transform(self, df):
        print("(transform) Drop columns: " + str(self.cols))
        return df.drop(self.cols, axis=1)
