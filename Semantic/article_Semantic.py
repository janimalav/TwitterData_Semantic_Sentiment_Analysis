from pymongo import MongoClient
from prettytable import PrettyTable
import math
import re

def main():
    table=PrettyTable()
    table.field_names=["Search Query","Document containing term(df)","N/(df)","Log10(N/df)"]
    client = MongoClient(
        "mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_reuters = client.reuter_data
    data_reuter=db_reuters.reuter

    reuter=data_reuter.find()

    totalDoc=0
    Canada=0
    rain=0
    cold=0
    rain_list=[]
    Canada_list=[]
    cold_list=[]
    for content in reuter:
        totalDoc+=1
        val_list_Canada=re.findall('\\bCanada\\b',content['body'])
        val_list_cold=re.findall('\\bcold\\b',content['body'])
        val_list_rain=re.findall('\\brain\\b',content['body'])
        if len(val_list_rain)!=0:
            rain_list.append(val_list_rain)
        if len(val_list_cold)!=0:
            cold_list.append(val_list_cold)
        if len(val_list_Canada)!=0:
            Canada_list.append(val_list_Canada)
    print("Total Documents:"+str(totalDoc))
    Canada=len(Canada_list)
    rain=len(rain_list)
    cold=len(cold_list)
    table.add_row(["Canada",Canada,totalDoc/Canada,math.log10(totalDoc/Canada)])
    table.add_row(["rain",rain,totalDoc/rain,math.log10(totalDoc/rain)])
    table.add_row(["cold",cold,totalDoc/cold,math.log10(totalDoc/cold)])
   
    print(table)

if __name__ == "__main__":
    main()