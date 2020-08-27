import os
import glob
import pandas as pd
import csv
os.chdir("/Users/amin/Development/station-data/pulled-data")
# os.chdir("/Users/amin/Development/station-data")

extension = 'csv'
all_filenames = [i for i in glob.glob("2*.csv")]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f,keep_default_na=False, na_values=['||||']) for f in all_filenames ])

#export to csv
combined_csv.to_csv( "combined_csv_2.csv", index=False, encoding='utf-8-sig')

input_file = open("combined_csv_2.csv","r+")
reader_file = csv.reader(input_file)
test = list(reader_file)
na2 = []

for row in test:
    na = []
    for item in row:
        na.append(item.replace("\xa0","").replace("w/m²","w/m sq"))
    na2.append(na)

with open('no_symbol_combined_csv.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(na2)

value = len(test)

print(value)


