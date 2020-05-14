import pandas as pd
import json
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import euclidean_distances

class ExportBookData(TransformerMixin):

    def __init__(self, mean_cols, books_df, authors_df, book_id_col='book_id',
                 dist_func=euclidean_distances, n_most_similar=5, mode='avg'):
        self.mean_cols = mean_cols
        self.books_df = books_df.copy()
        self.authors_df = authors_df.copy()
        self.book_id_col = book_id_col
        self.dist_func = dist_func
        self.n_most_similar = n_most_similar
        self.mode = mode

    def fit(self, df, y=None):
        
        def similar(x):
            index = x.name
            similar_books = similarity[index].nsmallest(self.n_most_similar + 1)[1:].index
            if self.mode == 'avg':
                return self.books_df[['text_reviews_count'] + self.mean_cols].loc[similar_books,:].mean()
            if self.mode == 'all':
                data = [r[col] for _, r in self
                        .books_df[['text_reviews_count'] + self.mean_cols].loc[similar_books, :].iterrows()
                        for col in ['text_reviews_count'] + self.mean_cols]
                cols = ['sim_' + str(i) + '_' + col for i in range(self.n_most_similar)
                        for col in ['text_reviews_count'] + self.mean_cols]
                response = pd.DataFrame(columns=cols)
                response.loc[0] = data
                return pd.Series(data, index=cols)
            raise ValueError('Invalid option for "mode" (valid options are "avg or "all')

        print('(fit) ExportBookData, mean_cols:', self.mean_cols,
              'book_id_col:', self.book_id_col, 'dist_func:', self.dist_func,
              'n_most_similar:', self.n_most_similar, 'mode:', self.mode)
        
        count = df[self.book_id_col].value_counts()
        self.books_df = self.books_df[self.books_df[self.book_id_col].isin(count.index)]
        self.books_df['text_reviews_count'] = count.values
        self.books_df = self.books_df.merge(df[[self.book_id_col] + self.mean_cols]
                                            .groupby(self.book_id_col).mean(), left_on='book_id',
                                 right_on='book_id')

        self.books_df["authors_names"] = [self.ExportAuthorNames(i) for i in self.books_df["authors"]]
        self.books_df["shelves_names"] = [self.ExportBookShelves(i) for i in self.books_df["popular_shelves"]]
        
        self.books_df['corpus'] = (pd.Series(self.books_df[['authors_names', 'description', 'shelves_names']].fillna('')
                .values.tolist()
                ).str.join(' '))
        
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, max_df=0.2, stop_words='english')
        tfidf_matrix = tf.fit_transform(self.books_df['corpus'])

        similarity = pd.DataFrame(data=self.dist_func(tfidf_matrix),
                                  columns=count.index, index=count.index)
        
        self.books_df = self.books_df.set_index("book_id")
        
        
        self.books_df = self.books_df.join(self.books_df.apply(similar, axis=1),
                                   rsuffix="_sim_" + self.mode)

        self.books_df = self.books_df.drop(['isbn', 'series', 'country_code', 'language_code',
                                  'popular_shelves', 'asin', 'is_ebook', 'average_rating',
                                  'kindle_asin', 'similar_books', 'description', 'format',
                                  'link', 'authors', 'publisher', 'num_pages', 'publication_day', 'isbn13',
                                  'publication_month', 'edition_information', 'publication_year', 'url',
                                  'image_url', 'ratings_count', 'work_id', 'title',
                                  'title_without_series', 'authors_names', 'shelves_names',
                                  'corpus'], axis=1)

        return self

    def transform(self, df):
        print('(transform) ExportBookData, mean_cols:', self.mean_cols,
              'book_id_col:', self.book_id_col, 'dist_func:', self.dist_func,
              'n_most_similar:', self.n_most_similar, 'mode:', self.mode)
        return df.join(df.apply(lambda x: self.books_df.loc[x[self.book_id_col], :],
                                axis=1), rsuffix="_book_avg")

    def ExportAuthorNames(self, x):
        response = ""
        for author in json.loads(x.replace('"','~').replace("'",'"').replace("~","'")):
            response += " " + self.authors_df[self.authors_df["author_id"] == int(author["author_id"])]["name"].values[0]
        return response
    
    def ExportBookShelves(self,x):
        response = ""
        for item in json.loads(x.replace("'",'"')):
            response += " " + item['name']
        return response

    
