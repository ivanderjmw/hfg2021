import csv
from abcd.models import *

def populate(addr):
    with open(addr, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (line_count != 0):
                print(f'{", ".join(row)}')
                temp = Assets(name=row[0], details=row[1], rating= 0 if row[2]=='' else row[2], 
                    address=row[3], contact=row[4])
                temp.save()
            line_count += 1
        print(f'Processed {line_count} lines.')
