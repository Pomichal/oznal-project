import pandas as pd
from sklearn.base import TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import euclidean_distances

class ExportBookData(TransformerMixin):

    def __init__(self, mean_cols, book_id_col='book_id',
                 dist_func=euclidean_distances, n_most_similar=5, mode='avg'):
        self.mean_cols = mean_cols
        self.book_id_col = book_id_col
        self.dist_func = dist_func
        self.n_most_similar = n_most_similar
        self.mode = mode
        self.books_df = pd.DataFrame()

    def fit(self, df, y=None):
        def similar(x):
            index = x.name
            similar_books = similarity[index].nsmallest(self.n_most_similar + 1)[1:].index
            if self.mode == 'avg':
                return self.books_df.loc[similar_books, ['row_count'] + self.mean_cols].mean()
            if self.mode == 'all':
                data = [r[col] for _, r in self
                        .books_df.loc[similar_books,
                                      ['row_count'] +self.mean_cols].iterrows()
                        for col in ['row_count'] + self.mean_cols]
                cols = ['sim_' + str(i) + '_' + col for i in range(self.n_most_similar)
                        for col in ['row_count'] + self.mean_cols]
                response = pd.DataFrame(columns=cols)
                response.loc[0] = data
                return pd.Series(data, index=cols)
            raise ValueError('Invalid option for "mode" (valid options are "avg or "all')

        print('(fit) ExportBookData, mean_cols:', self.mean_cols,
              'book_id_col:', self.book_id_col, 'dist_func:', self.dist_func,
              'n_most_similar:', self.n_most_similar, 'mode:', self.mode)
        count = df[self.book_id_col].value_counts()
        self.books_df['row_count'] = count
        self.books_df.index = count.index
        self.books_df = self.books_df.merge(df[[self.book_id_col] + self.mean_cols]
                                            .groupby(self.book_id_col).mean(),
                                            left_index=True, right_index=True)
        scaler = MinMaxScaler()
        similarity = pd.DataFrame(data=self.dist_func(scaler.fit_transform(self.books_df)),
                                  columns=count.index, index=count.index)
        self.books_df = self.books_df.join(self.books_df.apply(similar, axis=1),
                                           rsuffix="_sim_" + self.mode)
        return self

    def transform(self, df):
        print('(transform) ExportBookData, mean_cols:', self.mean_cols,
              'book_id_col:', self.book_id_col, 'dist_func:', self.dist_func,
              'n_most_similar:', self.n_most_similar, 'mode:', self.mode)
        return df.join(df.apply(lambda x: self.books_df.loc[x[self.book_id_col], :],
                                axis=1), rsuffix="_book_avg")
