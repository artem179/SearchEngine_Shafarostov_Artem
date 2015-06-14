import re
import argparse
import pymongo
from bson.son import SON
import os

import Parser

def find_occurences(query, collection, skip, limit):
    pipeline = [
            {"$match": {"$text": {"$search": query} } },
            {"$project": {'textScore': {'$meta': 'textScore'}, 'path': 1 } },
            {"$sort": SON([('textScore', {'$meta': 'textScore'})])},
            {"$skip": skip},
            {"$limit": limit}
            ]
    
    results = collection.aggregate(pipeline, allowDiskUse=True)
    #results = collection.find({'$text': {'$search': query}}, 
            #{'textScore': {'$meta': 'textScore'}, '_id': 1,
                #'path': 1})\
                        #.sort([('textScore', {'$meta': 'textScore'})])\
                        #.skip(skip)\
                        #.limit(limit)
    return list(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db-name', default='test_database',
            help='name of the database to connect to')
    parser.add_argument('--collection-name', default='texts',
            help='name of collection to connect to')
    parser.add_argument('--skip', default=0, type=int,
            help='number of results to skip')
    parser.add_argument('--limit', default=10, type=int,
            help='number of results to return')
    parser.add_argument('query', nargs=argparse.REMAINDER,
            help='text to be searched for')
    args = parser.parse_args()

    connection = pymongo.MongoClient()
    db = connection.get_database(args.db_name)
    collection = db.get_collection(args.collection_name)
    query = ' '.join(args.query)
    print(find_occurences(query, collection, args.skip, args.limit))
