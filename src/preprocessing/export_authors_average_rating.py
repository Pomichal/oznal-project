import json
import pandas as pd
from sklearn.base import TransformerMixin

class ExportAuthorsAverageRating(TransformerMixin):
    def __init__(self, author_col_name, new_col_name, authors_df):
        self.author_col_name = author_col_name
        self.new_col_name = new_col_name
        self.authors_df = authors_df

    def fit(self, df, y=None):
        print("(fit) Export authors average rating")
        return self

    def transform(self, df):
        print("(transform) Export authors average rating")
        authors_ratings = df[['book_id']]
        for book_id in df.book_id.unique():
            val = 0
            author_count = 0
            for author in json.loads(df[df.book_id == book_id][self.author_col_name].values[0]
                                     .replace('"','~').replace("'",'"').replace("~","'")):
                val += self.authors_df[self.authors_df['author_id'] ==
                                       int(author['author_id'])]['average_rating'].values[0]
                author_count += 1
            if author_count > 0:
                authors_ratings.loc[authors_ratings.book_id == book_id, self.new_col_name] = val / author_count
        authors_ratings.loc[:, self.new_col_name] = pd.to_numeric(authors_ratings[self.new_col_name])
        return df.join(authors_ratings[self.new_col_name])

