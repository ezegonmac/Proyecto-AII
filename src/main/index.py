from bs4 import BeautifulSoup
import urllib.request
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID, DATETIME
from whoosh.qparser import QueryParser
from main.scraping import scrape

def search_all_index():
    index = open_dir("Index")
    searcher = index.searcher()
    query = QueryParser("name", index.schema).parse("*")
    results = searcher.search(query, limit=None)
    
    return results


def load_data():
    items = scrape()
    index = create_database()
    load_database(index, items)

    return items


def create_database():
    schema = Schema(
        name=TEXT(stored=True, phrase=False),
        short_name=TEXT(stored=True, phrase=False),
        price=NUMERIC(stored=True, numtype=float),
        url=ID(stored=True),
        image=ID(stored=True),
        detail_image=ID(stored=True),
        description=TEXT(stored=True),
        brand=KEYWORD(stored=True, commas=True),
        type=KEYWORD(stored=True, commas=True),
        exterior_finishes=KEYWORD(stored=True, commas=True),
        plastic_colors=KEYWORD(stored=True, commas=True),
        internal_plastic_colors=KEYWORD(stored=True, commas=True),
        magnets=KEYWORD(stored=True, commas=True),
        size=NUMERIC(stored=True, numtype=float),
        weight=NUMERIC(stored=True, numtype=int),
        release_date=DATETIME(stored=True)
        )
    
    # remove old index
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    index = create_in("Index", schema=schema)
    
    return index


def load_database(index, items):
    writer = index.writer()
    
    for item in items:
        
        writer.add_document(
            name=item['name'],
            short_name=item['short_name'],
            price=item['price'],
            url=item['url'],
            image=item['image'],
            detail_image=item['detail_image'],
            description=item['description'],
            brand=item['brand'],
            type=item['type'],
            exterior_finishes=item['exterior_finishes'],
            plastic_colors=item['plastic_colors'],
            internal_plastic_colors=item['internal_plastic_colors'],
            magnets=item['magnets'],
            size=item['size'],
            weight=item['weight'],
            release_date=item['release_date']
            )

    writer.commit()
    print("###################################")
    print("Index created")
    print("Number of items: " + str(len(items)))
    print("###################################")
