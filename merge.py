import os
import glob
import pandas as pd
import csv
os.chdir("/Users/amin/Development/station-data/pulled-data")

extension = 'csv'
all_filenames = [i for i in glob.glob("2*.csv")]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f,keep_default_na=False, na_values=['||||']) for f in all_filenames ])

#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

input_file = open("combined_csv.csv","r+")
reader_file = csv.reader(input_file)
value = len(list(reader_file))

print(value)

