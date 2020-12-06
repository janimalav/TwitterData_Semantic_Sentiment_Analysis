from pymongo import MongoClient
from prettytable import PrettyTable
import re

def main():
    csvTable = PrettyTable(["Tweet ID","Message","+ve Words","-ve Words","Polarity"])

    positive_words_file = open("positive-words.txt", 'r')
    negative_words_file = open("negative-words.txt", 'r')

    positive_words = []
    negative_words = []

    for word in positive_words_file:
        positive_words.append(word.replace('\n', '').lower())

    for word in negative_words_file:
        negative_words.append(word.replace('\n', '').lower())
    
    client = MongoClient(
        "mongodb+srv://root:PKZJNrap80flRe3X@data.nrdnw.mongodb.net/clean_db?retryWrites=true&w=majority")
    db_processed = client.ProcessedDb
    data_search = db_processed.search_tweets
    data_stream=db_processed.stream_tweets

    tweetlist_search = data_search.find()
    tweetlist_stream=data_stream.find()
    
    row=[]
    value=[]
    BOW={}
    count=0

    for (count,tweet) in enumerate(tweetlist_search):
        count=count+1
        row=[]
        value=tweet['Content'].split(" ")
        row.append(count)
        row.append(tweet['Content'].replace("\n",' '))
        
        for word in value:
            word=word.replace("\n",' ')
            word=word.strip(",./;\'[]:{<>!@#$%^&*()}\n").lower()
            if word in BOW:
                BOW[word] = BOW[word]+1
            else:
                BOW[word]=1   
        positivewords=[]
        negativewords=[]
        for (bow_word,count) in BOW.items():
            if bow_word in positive_words:
                positivewords.append(bow_word)
            elif bow_word in negative_words:
                negativewords.append(bow_word)

        if len(positivewords) == 0:
            row.append("Not Found")
        else:
            row.append(positivewords)           
        if len(negativewords) == 0:
            row.append("Not Found")
        else:
            row.append(negativewords)

        if len(positivewords)>len(negativewords):
            row.append("Positive")
        elif len(positivewords)<len(negativewords):
            row.append("Negative")
        else:
            row.append("Neutral")
        csvTable.add_row(row)

    print(csvTable.get_csv_string())

    for (count,tweet) in enumerate(tweetlist_stream):
        row=[]
        count=count+1     
        row.append(count)
        value=tweet['Content'].split(" ")
        
        row.append(tweet['Content'])
        for word in value:
            word=word.replace("\n",'')
            word=word.strip(",./;\'[]:{<>!@#$%^&*()}\n").lower()
            if word in BOW:
                BOW[word] = BOW[word]+1
            else:
                BOW[word]=1   

        positivewords=[]
        negativewords=[] 
        for (bow_word,count) in BOW.items():
            if bow_word in positive_words:
                positivewords.append(bow_word)
            elif bow_word in negative_words:
                negativewords.append(bow_word)          
        
        if len(positivewords) == 0:
            row.append("Not Found")
        else:
            row.append(positivewords)           
        if len(negativewords) == 0:
            row.append("Not Found")
        else:
            row.append(negativewords)

        if len(positivewords)>len(negativewords):
            row.append("Positive")
        elif len(positivewords)<len(negativewords):
            row.append("Negative")
        else:
            row.append("Neutral")
        csvTable.add_row(row)
    print(csvTable)
    with open("sentiment.csv","w+",encoding="utf-8") as output:
        output.write(csvTable.get_csv_string())

if __name__ == "__main__":
    main()