import json
import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
from langdetect import detect
import re
from sklearn.base import clone
from sklearn.model_selection import cross_validate
import math
from scipy.stats import boxcox

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

