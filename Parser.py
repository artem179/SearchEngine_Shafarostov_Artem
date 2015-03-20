import re
import pymongo
import os
import sys
from bs4 import BeautifulSoup
from imp import reload
reload(sys)
sys.setdefaultencoding('utf-8')

from pymongo import Connection
connection = Connection()
connection.drop_database("test_database")
db = connection.test_database
db.drop_collection('books')

words = []

for top, dir, files in os.walk('/home/artem/az.lib.ru2/az.lib.ru/'):
    for a in files:
        path = os.path.join(top, a)
        document = open(path)
        parsered = BeautifulSoup(document)
        [x.extract() for x in parsered.findAll('script')]
        MeaningText = parsered.get_text().encode('utf-8')
        for s in MeaningText:
            r = re.split("[\s;:\-_*\".,?!()]", s)
            r = [a for a in r if a != '']
            words.extend(r)
        db.books.save({'Path' : path, 'Text' : MeaningText, 'Words' : words})
        document.close()

if __name__ == "__main__":
    print "Hi my dear friend. What do u want to know about this db ?"
    if len(sys.argv) != 3:
        print "Sorry but we don't have such command, try again"
    else:
        FirstWord = sys.argv[1]
        SecondWord = sys.argv[2]
        if FirstWord == 'sh' and SecondWord == 'elements':
            print db.books.count()
        elif FirstWord == 'sh' and SecondWord == 'rand':
            print db.books.find().limit(-1).skip(5).next()
        else:
            print "Sorry but we don't have such command, try again"
