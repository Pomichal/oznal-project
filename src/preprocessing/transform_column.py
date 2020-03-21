import json
import pandas as pd

class ColumnTransformer:

    def export_book_shelves(self, df, tag_column, tags):
        response = pd.DataFrame(columns=tags, index=df.index)
        for index, row in df.iterrows():
            shelves = json.loads(row[tag_column].replace("'",'"'))
            data = filter(lambda shelve: shelve['name'] in tags, shelves)
            for item in data:
                response.loc[index][item['name']] = item['count']
        return response
