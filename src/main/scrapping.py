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
    items = get_items(1)
    return items


def get_items(num_pages):
    items = []
    
    for page in range(0, num_pages):
        url = f'https://speedcubeshop.com/collections/cubes-puzzles-wca?page={page}'
        ctx1 = urllib.request.urlopen(url)
        s1 = BeautifulSoup(ctx1, "lxml")
        
        items_collection_div = s1.find("div", class_="product-collection")
        items_divs = items_collection_div.find_all("div", class_="inner product-item")
        for item_div in items_divs:
            item = parse_item(item_div)
            
            ctx2 = urllib.request.urlopen(item["url"])
            s2 = BeautifulSoup(ctx2, "lxml")
            item_details = parse_item_details(s2)
            
            item = {**item, **item_details}
            items.append(item)
   
    return items


def parse_item(item_div):
    item_name = item_div.find("a", class_="product-title").text
    item_price = item_div.find("div", class_="price-regular").text.replace("€", "").replace(",", ".")
    item_url = "https://speedcubeshop.com" + item_div.find("a", class_="product-title")["href"]
    item_picture = item_div.find("span", class_="images-two")
    item_image = item_picture.find("picture").find("source")["data-srcset"] if item_picture else ""
    
    item = {
        "name": item_name,
        "price": item_price,
        "url": item_url,
        "image": item_image,
        }
    
    return item


def parse_item_details(s2):
    
    product_top_div = s2.find("div", class_="product_top")
    product_bottom_div = s2.find("div", class_="product_bottom")
    
    item_detail_image = product_top_div.find("img")["data-src"]
    item_short_name = product_top_div.find("h1", class_="product-title").text
    item_brand = product_top_div.find("div", class_="vendor-product").find("a").text
    
    # colors
    item_product_variants_div = product_top_div.find("div", id="product-variants")
    item_color_variants_divs = item_product_variants_div.find("div", class_="swatch-content").find_all("div", class_="swatch-element")
    item_colors = [div["data-value"] for div in item_color_variants_divs]
    
    item_description = product_bottom_div.find("div", class_="rte").find("p").text
    
    # details
    item_details_div = product_bottom_div.find("div", class_="tab-content", id="collapse-tab3")
    detail_label_divs = item_details_div.find_all("label", class_="infodatalabel")
    detail_value_divs = item_details_div.find_all("label", class_="infolabel")
    
    for label, value in zip(detail_label_divs, detail_value_divs):
        if label.text == "Type":
            item_type = value.text
        elif label.text == "Magnets":
            item_magnets = value.text
        elif label.text == "Weight":
            item_weight = value.text.replace("g", "").strip()
        elif label.text == "Released":
            item_release_date = value.text
        else:
            print("Unknown detail: " + label.text)

    item_details = {
        "detail_image": item_detail_image,
        "short_name": item_short_name,
        "brand": item_brand,
        "colors": item_colors,
        "description": item_description,
        "type": item_type or "",
        "magnets": item_magnets or "",
        "weight": item_weight or None,
        "release_date": item_release_date or "",
        }
    
    return item_details