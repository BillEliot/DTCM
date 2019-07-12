import argparse, csv, sys
import sqlite3

connection = None
'''
data format:
Pinyin, ChineseName, EnglishName, Sort_id
'''
def importSortFromCSV(path):
    csv_file = csv.reader(open(path, 'r'))
    sortList = []
    for row in csv_file:
        sortList.append((row[0], row[1], row[2], row[3]))
    
    connection.executemany("INSERT INTO search_entry (PinyinName, SimplifiedName, EnglishName_1, Sort_id) VALUES (?,?,?,?)", sortList)
    connection.commit()
    connection.close()
    print('[+] 共添加%d条数据' % len(sortList))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import csv sort data into the database in batches, common csv data format is as follows:\n \
        Pinyin, ChineseName, [TraditionalName], EnglishName_1, [EnglishName_2], [EnglishName_3], Sort_id")
    parser.add_argument('path', help="the path of csv")
    args = parser.parse_args()
    # connect to sqllite
    connection = sqlite3.connect('../db.sqlite3')
    print('[+] Connect to sqlite successfully')
    importSortFromCSV(args.path)
