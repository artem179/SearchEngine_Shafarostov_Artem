import re
import argparse
import pymongo
import os
import codecs
from bs4 import BeautifulSoup

TEXT_FIELD = "content"
FILENAME_FIELD = "path"

def index_directory(directory_name, db_collection, **kwargs):
    for root, dir, files in os.walk(directory_name):
        for filename in files:
            path = os.path.join(root, filename)
            if db_collection.find({FILENAME_FIELD : path}).count() > 0 or \
                    (kwargs.get("filename_regex") and \
                    not re.fullmatch(kwargs["filename_regex"], filename)):
                    continue
            print("Indexing " + path)
            with codecs.open(path, 'r', encoding='cp1251') as document:
                parsed_document = BeautifulSoup(document)
                [x.extract() for x in parsed_document( ['style', 'script', '[document]', 'head', 'title'])]
                document_text = parsed_document.get_text()
                db_collection.save({FILENAME_FIELD : path,
                    TEXT_FIELD : document_text})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('directories', nargs='*', default=["./"],
            help='directories with files to be indexed')
    parser.add_argument('--db-name', default='test_database',
            help='name of the database to connect to')
    parser.add_argument('--collection-name', default='texts',
            help='name of collection to connect to')
    parser.add_argument('--filename-regex',
            help='filenames of files to be indexed must match the regex')
    parser.add_argument('--drop-index', action='store_true',
            help='delete previously indexed information from db')
    parser.add_argument('--default-language', default='english',
            help='language of documents to be stored in db.\
                    Effective only with --drop-index.')
    args = parser.parse_args()

    connection = pymongo.MongoClient()
    db = connection.get_database(args.db_name)
    collection = db.get_collection(args.collection_name)
    if args.drop_index:
        print("Deleting collection " + args.collection_name)
        db.drop_collection(args.collection_name)
        collection = db.get_collection(args.collection_name)
        collection.create_index(FILENAME_FIELD)
        collection.create_index([(TEXT_FIELD, 'text')],
                default_language=args.default_language)

    for directory_name in args.directories:
        index_directory(directory_name, collection,
                filename_regex=args.filename_regex)
