import re
import argparse
import pymongo
import os
import codecs
from bs4 import BeautifulSoup

def index_directory(directory_name, db_collection, **kwargs):
    for root, dir, files in os.walk(directory_name):
        for filename in files:
            path = os.path.join(root, filename)
            if kwargs.get("filename_regex") and \
                not re.fullmatch(kwargs["filename_regex"], filename):
                    continue
            print("Indexing " + path)
            with codecs.open(path, 'r', encoding='cp1251') as document:
                parsed_document = BeautifulSoup(document)
                [x.extract() for x in parsed_document( ['style', 'script', '[document]', 'head', 'title'])]
                document_text = parsed_document.get_text()
                words = []
                for line in document_text:
                    r = re.split("[\s;:\-_*\".,?!()]", line)
                    r = [a for a in r if a != '']
                    words.extend(r)
                db_collection.save({'Path' : path, 'Text' : document_text})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='*',
            help='directories with html files to be indexed')
    parser.add_argument('--drop-index', action='store_true',
            help='delete previously indexed information from db')
    parser.add_argument('--db-name', default='test_database',
            help='name of the database to connect to')
    parser.add_argument('--collection-name', default='texts',
            help='name of collection to connect to')
    parser.add_argument('--filename-regex',
            help='filenames of files to be indexed must match the regex')
    args = parser.parse_args()

    connection = pymongo.MongoClient()
    db = connection.get_database(args.db_name)
    if args.drop_index:
        print("Deleting collection " + args.collection_name)
        db.drop_collection(args.collection_name)
    collection = db.get_collection(args.collection_name)

    for directory_name in args.directories:
        index_directory(directory_name, collection,
                filename_regex=args.filename_regex)
