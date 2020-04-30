import json
import pandas as pd
from sklearn.base import TransformerMixin

class ExportBookShelves(TransformerMixin):

    def __init__(self, tag_column, tags):
        self.tag_col = tag_column
        self.tags = tags

    def fit(self, df, y=None):
        print('(fit) ExportBookShelves, tag_col: ' + self.tag_col + ', tags:' + str(self.tags))
        return self

    def transform(self, df):
        print('(transform) ExportBookShelves, tag_col: ' + self.tag_col + ', tags:' + str(self.tags))
        new_cols = df[['book_id']]
        for book_id in df.book_id.unique():
            shelves = json.loads(df[df.book_id == book_id][self.tag_col].values[0].replace("'",'"'))
            data = filter(lambda shelve: shelve['name'] in self.tags, shelves)
            for item in data:
                new_cols.loc[new_cols.book_id == book_id,item['name']] = item['count']
        new_cols = new_cols.fillna(value={i : 0 for i in self.tags})
        for col in new_cols:
            new_cols.loc[:,col] = pd.to_numeric(new_cols[col])
        return df.join(new_cols.drop(['book_id'], axis=1))
