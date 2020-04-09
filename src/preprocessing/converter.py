#!/usr/bin/python3.7

import pandas as pd
import sys, getopt

helpstring = 'usage: converter.py -i <inputfile_json> -o <outputfile_location> [-c <chunksize>]'

def main(argv):
    inputfile = ''
    outputfile = ''
    chunksize = 10000
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(helpstring);
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpstring)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-c", "--chunksize"):
            chunksize = arg
    json_to_csv(inputfile, outputfile, chunksize)


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

if __name__ == "__main__":
   main(sys.argv[1:])
