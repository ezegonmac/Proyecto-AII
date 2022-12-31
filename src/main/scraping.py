from bs4 import BeautifulSoup
import urllib.request
import ssl, os
import re
from datetime import datetime

# avoid SSL error
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def scrape():
    # max 15 WCA pages
    # max 48 ALL pages
    items = get_items(47)
    return items


def get_items(num_pages):
    items = []

    for page in range(0, num_pages):
        print(f'page {page}/{num_pages}')
        url = f'https://speedcubeshop.com/collections/all-puzzles?page={page}'
        ctx1 = urllib.request.urlopen(url)
        s1 = BeautifulSoup(ctx1, "lxml")

        items_collection_div = s1.find("div", class_="product-collection")
        items_divs = items_collection_div.find_all("div", class_="inner product-item")
        for item_div in items_divs:
            try:
                item = parse_item(item_div)
            except Exception as e:
                print(f"Error parsing item {item_div.text}")
                print(e)
                continue

            ctx2 = urllib.request.urlopen(item["url"])
            s2 = BeautifulSoup(ctx2, "lxml")
            
            try:
                item_details = parse_item_details(s2)
            except Exception as e:
                print(f"Error parsing item details for {item['name']}")
                print(e)
                continue

            item = {**item, **item_details}
            items.append(item)

    return items


def parse_item(item_div):
    item_name = item_div.find("a", class_="product-title").text.strip()
    item_price = item_div.find("div", class_="price-regular").text.replace("€", "").replace(",", ".").replace("starting at", "").strip()
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
    item_short_name = product_top_div.find("h1", class_="product-title").text.strip()
    item_brand = product_top_div.find("div", class_="vendor-product").find("a").text.strip()

    # variants
    item_product_variants_divs = product_top_div.find("div", id="product-variants").find_all("div", class_="swatch")
    item_exterior_finishes = ""
    item_plastic_colors = ""
    item_internal_plastic_colors = ""
    for div in item_product_variants_divs:
        label = div.find("div", class_="header").find("span").text.strip()
        values_divs = div.find("div", class_="swatch-content").find_all("div", class_="swatch-element")
        values = [div["data-value"].strip() for div in values_divs]

        if label.strip() == "Exterior Finish":
            item_exterior_finishes = values
        elif label.strip() == "Plastic Color":
            item_plastic_colors = values
        elif label.strip() == "Internal Plastic Color":
            item_internal_plastic_colors = values
        else :
            print("Unknown variant: " + label)

    rte_div = product_bottom_div.find("div", class_="rte")
    item_description = rte_div.find("p")
    if not item_description:
        item_description = rte_div.text
    else :
        item_description = item_description.text.strip()

    # details
    item_details_div = product_bottom_div.find("div", class_="tab-content", id="collapse-tab3")
    detail_label_divs = item_details_div.find_all("label", class_="infodatalabel")
    detail_value_divs = item_details_div.find_all("label", class_="infolabel")

    item_type = ""
    item_magnets = ""
    item_size = ""
    item_weight = ""
    item_release_date = ""
    for label, value in zip(detail_label_divs, detail_value_divs):
        if label.text.strip() == "Type":
            item_type = value.text.strip()
        elif label.text.strip() == "Magnets":
            item_magnets = value.text.strip()
        elif label.text.strip() == "Size":
            value = value.text.replace("mm", "").strip()
            if re.search(r'\d+?\.?\d+', value):
                item_size = float(value) if value else None
            else:
                item_size = None
        elif label.text.strip() == "Weight":
            value = value.text.replace("g", "").strip()
            item_weight = float(value) if value else None
        elif label.text.strip() == "Released":
            value = value.text.strip()
            item_release_date = datetime.strptime(value, '%Y-%m-%d') if value else None 
        else:
            print("Unknown detail: " + label.text + " - " + item_short_name)

    item_details = {
        "detail_image": item_detail_image,
        "short_name": item_short_name,
        "brand": item_brand,
        "exterior_finishes": item_exterior_finishes,
        "plastic_colors": item_plastic_colors,
        "internal_plastic_colors": item_internal_plastic_colors,
        "description": item_description,
        "type": item_type,
        "magnets": item_magnets,
        "size": item_size,
        "weight": item_weight,
        "release_date": item_release_date,
        }

    return item_details
