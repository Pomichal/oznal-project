import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin

class ExportSimilarBooksRating(TransformerMixin):
    def __init__(self, books_df, col_name, new_col_name):
        self.books_df = books_df
        self.col_name = col_name
        self.new_col_name = new_col_name

    def fit(self, df, y=None):
        print("(fit) Export similar books average rating")
#         self.books_df = self.books_df.loc[df.index]    # ???
        return self

    def transform(self, df):
        print("(transform) Export similar books average rating")
        def export_avg_rating_from_list(id_list, books_df):
            mean = np.nan
            if(id_list != "[]"):
                ids = [int(i) for i in id_list.strip('][').replace("'","").split(', ')]
                mean = books_df[books_df['book_id'].isin(ids)].average_rating.mean()
            return mean

        similar_books_ratings = pd.DataFrame(columns=[self.new_col_name], index=df.index)
        similar_books_ratings[self.new_col_name] = df[self.col_name].apply(export_avg_rating_from_list,
                                                                           args=(self.books_df,))
        return df.join(similar_books_ratings)
