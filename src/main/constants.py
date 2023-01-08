from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SCRAPING

NUM_PAGES_TO_SCRAPE = 47 # max 48 ALL pages


# INDEX

INDEX_FOLDER = BASE_DIR + "/Index"
INDEX_ITEMS = "items_index"
INDEX_BRANDS = "brands_index"
INDEX_TYPES = "types_index"
INDEX_MAGNETS = "magnets_index"
INDEX_EXTERIOR_FINISH = "exterior_finishes_index"
INDEX_PLASTIC_COLOR = "plastic_colors_index"
INDEX_INTERIOR_PLASTIC_COLOR = "interior_plastic_colors_index"

# RECOMMENDATIONS

ATTRIBUTES_WEIGHTS = {
    "short_name": 3.0,
    "price": 6.0,
    "brand": 7.0,
    "type": 7.0,
    "magnets": 4.0,
    "size": 0.1,
    "weight": 0.1,
    "exterior_finishes": 0.1,
    "plastic_colors": 0.1,
    "internal_plastic_colors": 0.1,
    }
