from pymongo import MongoClient
from prettytable import PrettyTable
import math
import re

def main():
    table=PrettyTable()
    table.field_names=["Canada appeared in Document","Total Words","Frequency"]
    client = MongoClient(
        "mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_reuters = client.reuter_data
    data_reuter=db_reuters.reuter

    reuter=data_reuter.find()

    totalDoc=0
    highest_f=0.0
    for content in reuter:
        totalDoc+=1
        if "Canada" in content['body'] or "Canada" in content['title'] or "Canada" in content['dateline']:
            documentCount=len(content['body'].split(" "))+len(content['title'].split(" "))+len(content['dateline'].split(" "))
            val_list_Canada=re.findall('Canada',content['body'])
            m=documentCount
            f=len(val_list_Canada)
            if (f/m) > highest_f:
                highest_f=f/m
            table.add_row(["Document # "+str(totalDoc),documentCount,len(val_list_Canada)])
            
   
    print(table)
    print("Highest Relative Frequency is "+str(highest_f))

if __name__ == "__main__":
    main()