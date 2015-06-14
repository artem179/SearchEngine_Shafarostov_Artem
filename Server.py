from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash
import pymongo
import Search

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

client = pymongo.MongoClient()
db = client.test_database
collection = db.texts

@app.route('/')
def search():
    query = request.args.get('query')
    page = request.args.get('page') or '1'
    page = int(page)
    found = []
    if query:
        found = Search.find_occurences(query, collection, (page - 1) * 10, 10)
    return render_template('search.html', found=found, page=page)

if __name__ == "__main__":
    app.run()
