from sklearn.base import TransformerMixin

class ReviewLengthFilter(TransformerMixin):
    def __init__(self, column, lower_boundary, upper_boundary):
        self.column = column
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary

    def fit(self, df, y=None, **fit_params):
        print("(fit) Review length filter")
        return self

    def transform(self, df, **transform_params):
        print("(transform) Review length filter")
        df_copy = df.copy()

        df_copy['num_words'] = df_copy[self.column].apply(
            lambda text: len(text.split())
        )
        df_copy = df_copy[
            (df_copy['num_words'] > self.lower_boundary) & (df_copy['num_words'] < self.upper_boundary)
        ]

        df_copy.drop(['num_words'], axis=1, inplace=True)

        return df_copy
