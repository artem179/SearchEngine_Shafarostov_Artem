import re
import argparse
import pymongo
import os

import Parser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db-name', default='test_database',
            help='name of the database to connect to')
    parser.add_argument('--collection-name', default='texts',
            help='name of collection to connect to')
    parser.add_argument('query',
            help='text to be searched for')
    args = parser.parse_args()

    connection = pymongo.MongoClient()
    db = connection.get_database(args.db_name)
    collection = db.get_collection(args.collection_name)
    results = collection.find({"$text": {"$search": args.query}})
    print(results.count())
    for result in results:
        print(result[Parser.FILENAME_FIELD])
