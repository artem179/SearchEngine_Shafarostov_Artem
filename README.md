# Small search engine
A tiny search engine based on mongodb.

## What do I need
You need the following apps installed:

1. Python 3
2. MongoDB
3. Virtualenv

## How to install
```
$ git clone https://github.com/cs-hse-projects/SearchEngine_Shafarostov_Artem.git
$ cd SearchEngine_Shafarostov_Artem
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

## How to use
There are two main files in this project: `Indexer.py` and `Search.py`.

`Indexer.py` is a module that contains only one function: `index_directory`,
that adds all files from the specified directory to the database. You could also
run `python Indexer.py` with arguments and it will index the given directories.
Run `python Indexer.py --help` for more info on accepted arguments.
On the first run, `--drop-index` must be used to ensure that the database
has the right schema.
If indexer is run with `--use-pymorophy`, then before adding
each file to the database, it normalizes each word in the text using `pymorphy2`.

`Search.py` is a module with one function: `find_occurences`, that accepts the string
that you want to find in the database and returns the list of all documents containing
given string. Text is being searched using mongodb's text indexes, and it behaves like
described [here](http://docs.mongodb.org/manual/reference/operator/query/text/#search-field).
So, for example, if you want to search for a phrase `good morning`, you have to pass string
`"\"good morning\""` to the find_occurences function.
`Search.py` can also be used as a script, run `python Search.py --help` for more info.

## Web interface
In file `Server.py` a tiny web interface for `Search.py` is implemented. To use it,
issue `python Server.py`, then go to [127.0.0.1:5000](http://127.0.0.1:5000)
(or another address that will be suggested to you after you run `Server.py`).
