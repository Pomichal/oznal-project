import json
import pandas as pd
from sklearn.base import TransformerMixin

class ColumnTransformer:

    def export_book_shelves(self, df, tag_column, tags):
        response = pd.DataFrame(columns=tags, index=df.index)
        for index, row in df.iterrows():
            shelves = json.loads(row[tag_column].replace("'",'"'))
            data = filter(lambda shelve: shelve['name'] in tags, shelves)
            for item in data:
                response.loc[index][item['name']] = item['count']
        return response

    def export_book_authors_average_value(self, df, authors_df, col_name='average_rating', new_col_name='authors_average_rating'):
        response = pd.DataFrame(columns=[new_col_name], index=df.index)
        for index, row in df.iterrows():
            val = 0
            author_count = 0
            for author in json.loads(row.loc['authors'].replace('"','~').replace("'",'"').replace("~","'")):
                val += authors_df[authors_df['author_id'] == int(author['author_id'])][col_name].values[0]
                author_count += 1
            if author_count > 0:
                response.loc[index][new_col_name] = val / author_count
        return response


class ExportBookShelves(TransformerMixin):

    def __init__(self, tag_column, tags):
        self.tag_col = tag_column
        self.tags = tags

    def fit(self, df, y=None):
        print('(fit) ExportBookShelves, tag_col: ' + self.tag_col + ', tags:' + str(self.tags))
        return self

    def transform(self, df):
        new_cols = pd.DataFrame(columns=self.tags, index=df.index)
        for index, row in df.iterrows():
            shelves = json.loads(row[self.tag_col].replace("'",'"'))
            data = filter(lambda shelve: shelve['name'] in self.tags, shelves)
            for item in data:
                new_cols.loc[index][item['name']] = item['count']
        new_cols = new_cols.fillna(value={i : 0 for i in self.tags})
        for col in new_cols:
            new_cols[col] = pd.to_numeric(new_cols[col])
        return df.join(new_cols)


class DropColumns(TransformerMixin):
    def __init__(self, cols):
        self.cols = cols

    def fit(self, df, y=None):
        print("(fit) Drop columns: " + str(self.cols))
        return self

    def transform(self, df):
        return df.drop(self.cols, axis=1)


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
        return df[df[self.col_name] >= self.bound]


class ExportAuthorsAverageRating(TransformerMixin):
    def __init__(self, author_col_name, new_col_name, authors_df):
        self.author_col_name = author_col_name
        self.new_col_name = new_col_name
        self.authors_df = authors_df

    def fit(self, df, y=None):
        print("(fit) Export authors average rating")
        return self

    def transform(self, df):
        authors_ratings = pd.DataFrame(columns=[self.new_col_name], index=df.index)
        for index, row in df.iterrows():
            val = 0
            author_count = 0
            for author in json.loads(row.loc[self.author_col_name].replace('"','~').replace("'",'"').replace("~","'")):
                val += self.authors_df[self.authors_df['author_id'] == 
                                       int(author['author_id'])]['average_rating'].values[0]
                author_count += 1
            if author_count > 0:
                authors_ratings.loc[index][self.new_col_name] = val / author_count
                
        return df.join(authors_ratings)
