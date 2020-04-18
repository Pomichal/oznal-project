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


class ExportBookShelves(TransformerMixin):

    def __init__(self, tag_column, tags):
        self.tag_col = tag_column
        self.tags = tags

    def fit(self, df, y=None):
        print('(fit) ExportBookShelves, tag_col: ' + self.tag_col + ', tags:' + str(self.tags))
        return self

    def transform(self, df):
        print('(transform) ExportBookShelves, tag_col: ' + self.tag_col + ', tags:' + str(self.tags))
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
        print("(transform) Drop columns: " + str(self.cols))
        return df.drop(self.cols, axis=1)


class DropValues(TransformerMixin):
    def __init__(self, col_names, filter_func):
        self.col_names = col_names
        self.func = filter_func

    def fit(self, df, y=None, **fit_params):
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            df_copy = df_copy[self.func(df_copy, col)]
        return df_copy


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
        authors_ratings[self.new_col_name] = pd.to_numeric(authors_ratings[self.new_col_name])
        return df.join(authors_ratings)


class EncodeCategories(TransformerMixin):
    def __init__(self, encoder):
        self.encoder = encoder

    def fit(self, df, y=None):
        print("(fit) Category encoder " + str(self.encoder))
        self.encoder.fit(df)
        return self

    def transform(self, df):
        print("(transform) Category encoder " + str(self.encoder))
        df_copy = df.copy()
        df_copy = self.encoder.transform(df)
        return df_copy


class ReviewsLanguageFilter(TransformerMixin):
    def __init__(self, column, language):
        self.column = column
        self.language = language

    def fit(self, df, y=None, **fit_params):
        print("(fit) Reviews language filter")
        return self

    def transform(self, df, **transform_params):
        def detect_text(text):
            try:
                return detect(text)
            except:
                return 'unknown'
        print("(transform) Reviews language filter")
        df_copy = df.copy()

        df_copy['lang'] = df_copy[self.column].apply(
            detect_text
        )
        df_copy = df_copy[df_copy.lang == self.language]

        df_copy.drop(['lang'], axis=1, inplace=True)

        return df_copy


class EmptyValuesFilter(TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, df, y=None, **fit_params):
        print("(fit) Empty values filter")
        return self

    def transform(self, df, **transform_params):
        print("(transform) Empty values filter")
        df = df.dropna(subset=self.columns)

        for column in self.columns:
            df = df[df[column] != '']

        return df


class TextPreprocessor(TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, df, y=None, **fit_params):
        print("(fit) Text preprocessing")
        return self

    def transform(self, df, **transform_params):
        print("(transform) Text preprocessing")
        df_copy = df.copy()

        # Lowercase text
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: text.lower()
        )
        # Remove special characters
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: re.sub(r'[^a-zA-Z0-9\.,?!]+', ' ', text)
        )
        # Remove urls
        df_copy[self.column] = df_copy[self.column].apply(
            lambda text: re.sub(r'(www|http:|https:)+[^\s]+[\w]', '', text)
        )

        return df_copy


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


class ReplaceNansNumeric(TransformerMixin):
    def __init__(self, col_names, func_type = 'median'):
        self.col_names = col_names
        self.func_type = func_type

    def fit(self, df, y=None, **fit_params):
        self.na_replace = {}
        for col in self.col_names:
            if(self.func_type == 'median'):
                self.na_replace[col] = df[col].median()
            else:
                self.na_replace[col] = df[col].mean()
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            df_copy[col] = df_copy[col].fillna(self.na_replace[col])
        return df_copy


class ReplaceOutliersWithPercentile(TransformerMixin):
    def __init__(self, col_names, upper_percentile, lower_percentile):
        self.col_names = col_names
        self.upper_percentile = upper_percentile
        self.lower_percentile = lower_percentile

    def fit(self, df, y=None, **fit_params):
        print('(fit) Replace outliers for: ',self.col_names, 'with percentiles: (', self.lower_percentile,
              self.upper_percentile, ")")
        self.min_extreme = {}
        self.max_extreme = {}
        self.min_replace = {}
        self.max_replace = {}
        for col in self.col_names:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.min_replace[col] = df[col].quantile(self.lower_percentile)
            self.max_replace[col] = df[col].quantile(self.upper_percentile)
            self.min_extreme[col] = (Q1 - 1.5 * IQR)
            self.max_extreme[col] = (Q3 + 1.5 * IQR)                   
        return self

    def transform(self, df, **transform_params):
        print('(fit) Replace outliers for: ',self.col_names, 'with percentiles: (', self.lower_percentile,
              self.upper_percentile, ")")
        df_copy = df.copy()
        for col in self.col_names:
            extremes_min = df_copy[df_copy[col] < self.min_extreme[col]].index
            extremes_max = df_copy[df_copy[col] > self.max_extreme[col]].index
            df_copy.loc[extremes_min, col] = self.min_replace[col]
            df_copy.loc[extremes_max, col] = self.max_replace[col]
        return df_copy


class DropOutliers(TransformerMixin):
    def __init__(self, col_names):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print('-- Drop outliers for: ',self.col_names)
        self.min_extreme = {}
        self.max_extreme = {}
        for col in self.col_names:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            self.min_extreme[col] = (Q1 - 1.5 * IQR)
            self.max_extreme[col] = (Q3 + 1.5 * IQR)                   
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            extremes_min = df_copy[df_copy[col] < self.min_extreme[col]].index
            extremes_max = df_copy[df_copy[col] > self.max_extreme[col]].index
            df_copy.drop(extremes_min, inplace=True)
            df_copy.drop(extremes_max, inplace=True)
        return df_copy


class ZScoreNormalization(TransformerMixin):
    def __init__(self, col_names):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) ZScoreNormalization")
        self.mean = {}
        self.std = {}
        for col in self.col_names:
            self.mean[col] = df[col].mean()
            self.std[col] = df[col].std()
        return self

    def transform(self, df, **transform_params):
        print("(transform) ZScoreNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = (df[col] - self.mean[col]) / self.std[col]
            df_copy[col] = transformed
        return df_copy


class LogNormalization(TransformerMixin):
    def __init__(self, col_names, new_name=""):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) LogNormalization")
        return self

    def transform(self, df, **transform_params):
        print("(transform) LogNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = df[col].apply(math.log)
            df_copy[col] = transformed
        return df_copy


class BoxCoxNormalization(TransformerMixin):
    def __init__(self, col_names, new_name=""):
        self.col_names = col_names

    def fit(self, df, y=None, **fit_params):
        print("(fit) LogNormalization")
        self.boxcox_attr = {}
        for col in self.col_names:
            _, self.boxcox_attr[col] = boxcox(df[col])
        return self

    def transform(self, df, **transform_params):
        print("(transform) LogNormalization")
        df_copy = df.copy()
        for col in self.col_names:
            transformed = boxcox(df_copy[col], lmbda=self.boxcox_attr[col])
            df_copy[col] = transformed
        return df_copy


class Scale(TransformerMixin):
    def __init__(self, col_names, scaler):
        self.col_names = col_names
        self.scaler = scaler

    def fit(self, df, y=None, **fit_params):
        self.scalers = {}
        for col in self.col_names:
            self.scalers[col] = clone(self.scaler).fit(df[col])
        return self

    def transform(self, df, **transform_params):
        df_copy = df.copy()
        for col in self.col_names:
            df_copy[col] = self.scalers[col].transform(df_copy[col])
        return df_copy
