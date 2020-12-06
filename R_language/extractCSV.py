from pymongo import MongoClient
import csv
import time
from datetime import datetime
import time
from prettytable import PrettyTable

def main():
    csvTable=PrettyTable(["dateTime","time"])
    client = MongoClient(
        "mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_processed = client.ProcessedDb
    data_search = db_processed.search_tweets
    data_stream=db_processed.stream_tweets

    tweetlist_search = data_search.find()
    tweetlist_stream=data_stream.find()
    for tweet in tweetlist_search:
        row=[]
        value=tweet['Timestamp']
        if value!='':
            date_obj = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
            date=date_obj.date()
            date1=date.timetuple()
            date_timeStamp=time.mktime(date1)
            times=datetime.timestamp(date_obj)
            row.append(date_timeStamp)
            row.append(times)
            csvTable.add_row(row)
        else:
            continue
        if 'Content - Original Tweet' in tweet:
            row=[]
            value=tweet['Timestamp - Original Tweet']
            if value!='':
                date_obj = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
                date=date_obj.date()
                date1=date.timetuple()
                date_timeStamp=time.mktime(date1)
                times=datetime.timestamp(date_obj)
                row.append(date_timeStamp)
                row.append(times)
                csvTable.add_row(row)
    with open("timestamp.csv","w+",encoding="utf-8") as output:
        output.write(csvTable.get_csv_string())
    print("done")
if __name__ == "__main__":
    main()
