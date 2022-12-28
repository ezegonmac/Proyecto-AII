from bs4 import BeautifulSoup
import urllib.request
# from tkinter import *
# from tkinter import messagebox
# import sqlite3
# import lxml

# avoid SSL error
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def scrape():
    items = get_items(2)
    return items

def get_items(num_pages):
    items=[]
    
    for page in range(0, num_pages):
        url = f'https://speedcubeshop.com/collections/cubes-puzzles-wca?page={page}'
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, "lxml")
        items_collection_div = s.find_all("div", class_="product-collection")
                
        for item in items_collection_div[0].find_all("div", class_="inner product-item"):
            
            item_name = item.find("a", class_="product-title").text
            item_price = item.find("div", class_="price-regular").text
            item_url = item.find("a", class_="product-title")["href"]
            item_picture = item.find("span", class_="images-two")
            item_image = item_picture.find("picture").find("source")["data-srcset"] if item_picture else ""
            
            item = {
                "name": item_name, 
                "price": item_price, 
                "url": item_url, 
                "image": item_image
                }
            items.append(item)
   
    return items
