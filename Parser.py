import re
import argparse
import pymongo
import os
import codecs
import pymorphy2
from bs4 import BeautifulSoup

TEXT_FIELD = "content"
FILENAME_FIELD = "path"
LANGUAGE_FIELD = "language"

def index_directory(directory_name, db_collection, language='english',
        **kwargs):
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
                [x.extract() for x in parsed_document(
                    ['style', 'script', '[document]', 'head', 'title'])]
                document_text = parsed_document.get_text().lower()
                if kwargs.get("morph"):
                    words = re.split('[^\w\d]', document_text)
                    morph = kwargs.get("morph")
                    result = ''
                    for word in words:
                        result += ' ' + morph.parse(word)[0].normal_form
                    document_text = result

                db_collection.save({FILENAME_FIELD : path,
                    TEXT_FIELD : document_text, LANGUAGE_FIELD : language})

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
    parser.add_argument('--language', default='english',
            help='language of documents to be added to db.\
                    This value will be set as default language of the\
                    collection when called with `--drop-index`.')
    args = parser.parse_args()

    connection = pymongo.MongoClient()
    db = connection.get_database(args.db_name)
    collection = db.get_collection(args.collection_name)
    if args.drop_index or not (args.collection_name in db.collection_names()):
        print("Deleting collection '%s'" % args.collection_name)
        db.drop_collection(args.collection_name)
        collection = db.get_collection(args.collection_name)
        collection.create_index(FILENAME_FIELD)
        collection.create_index([(TEXT_FIELD, 'text')],
                default_language=args.language)

    morph = None
    if args.language == 'ru' or args.language == 'russian':
        morph = pymorphy2.MorphAnalyzer()

    for directory_name in args.directories:
        index_directory(directory_name, collection,
                language=args.language,
                filename_regex=args.filename_regex,
                morph=morph)
