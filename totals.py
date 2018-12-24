import csv

theme = {}

with open('genesis-usage.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        theme[row[2]]++

