import pandas as pd

class Converter():

    # json data to csv
    def json_to_csv(source, destination, chunksize=10000):
        reader = pd.read_json(source, lines=True, chunksize=chunksize)
        first = True
        num_lines = sum(1 for line in open(source))
        num_chunks = num_lines // chunksize
        for chunk in reader:
            if first:
                chunk.to_csv(destination + '.csv', index=None)
                first = False
            else:
                chunk.to_csv(destination + '.csv', mode='a', header=False, index=None)
            print('chunks left: ' + str(num_chunks))
            num_chunks -= 1
        print()

