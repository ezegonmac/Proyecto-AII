import os
import shutil

from whoosh import index
from whoosh.fields import DATETIME, ID, KEYWORD, NUMERIC, TEXT, Schema
from whoosh.filedb.filestore import FileStorage
from whoosh.writing import AsyncWriter
from whoosh.analysis import LowercaseFilter, RegexTokenizer

from main.constants import INDEX_FOLDER
from main.index_details_search import (get_brands_ids_by_name,
                                       get_exterior_finishes_ids_by_name,
                                       get_interior_plastic_colors_ids_by_name,
                                       get_magnets_ids_by_name,
                                       get_plastic_colors_ids_by_name,
                                       get_types_ids_by_name)
from main.scraping import scrape
from main.constants import INDEX_ITEMS, INDEX_BRANDS, INDEX_TYPES, INDEX_MAGNETS, INDEX_EXTERIOR_FINISH, INDEX_PLASTIC_COLOR, INDEX_INTERIOR_PLASTIC_COLOR


def load_data():
    items, details_options = scrape()

    ix, details_ixs = create_indexes()

    load_index_details(details_ixs, details_options)
    load_index_data(ix, items)

    return items


def create_indexes():

    # Create an analyzer for searching that lowercases the input
    analyzer = RegexTokenizer() | LowercaseFilter()

    item_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False, analyzer=analyzer),
        short_name=TEXT(stored=True, phrase=False, analyzer=analyzer),
        price=NUMERIC(stored=True, numtype=float),
        url=ID(stored=True),
        image=ID(stored=True),
        detail_image=ID(stored=True),
        description=TEXT(stored=True, analyzer=analyzer),
        exterior_finishes=KEYWORD(stored=True, commas=True),
        plastic_colors=KEYWORD(stored=True, commas=True),
        internal_plastic_colors=KEYWORD(stored=True, commas=True),
        brand=ID(stored=True),
        type=ID(stored=True),
        magnets=ID(stored=True),
        size=NUMERIC(stored=True, numtype=float),
        weight=NUMERIC(stored=True, numtype=float),
        release_date=DATETIME(stored=True)
        )

    brand_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    type_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    magnets_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    exterior_finish_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    plastic_color_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    interior_plastic_color_schema = Schema(
        id=NUMERIC(stored=True, unique=True, numtype=int),
        name=TEXT(stored=True, phrase=False)
    )

    # remove old index
    if os.path.exists(INDEX_FOLDER):
        shutil.rmtree(INDEX_FOLDER)
    os.mkdir(INDEX_FOLDER)

    storage = FileStorage(INDEX_FOLDER)

    ix = index.create_in(INDEX_FOLDER, item_schema, indexname=INDEX_ITEMS)

    ix_brands = index.create_in(INDEX_FOLDER, brand_schema, indexname=INDEX_BRANDS)
    ix_types = index.create_in(INDEX_FOLDER, type_schema, indexname=INDEX_TYPES)
    ix_magnets = index.create_in(INDEX_FOLDER, magnets_schema, indexname=INDEX_MAGNETS)
    ix_exterior_finishes = index.create_in(INDEX_FOLDER, exterior_finish_schema, indexname=INDEX_EXTERIOR_FINISH)
    ix_plastic_colors = index.create_in(INDEX_FOLDER, plastic_color_schema, indexname=INDEX_PLASTIC_COLOR)
    ix_interior_plastic_colors = index.create_in(INDEX_FOLDER, interior_plastic_color_schema, indexname=INDEX_INTERIOR_PLASTIC_COLOR)
    details_ixs = {'ix_brands': ix_brands, 'ix_types': ix_types, 'ix_magnets': ix_magnets, 'ix_exterior_finishes': ix_exterior_finishes, 'ix_plastic_colors': ix_plastic_colors, 'ix_interior_plastic_colors': ix_interior_plastic_colors}

    return ix, details_ixs


def load_index_data(index, items):
    writer = index.writer()

    # get ids by name dicts
    brands_ids_by_name = get_brands_ids_by_name()
    types_ids_by_name = get_types_ids_by_name()
    magnets_ids_by_name = get_magnets_ids_by_name()
    exterior_finishes_ids_by_name = get_exterior_finishes_ids_by_name()
    plastic_colors_ids_by_name = get_plastic_colors_ids_by_name()
    interior_plastic_colors_ids_by_name = get_interior_plastic_colors_ids_by_name()

    for i in range(len(items)):

        item = items[i]

        # get ids for item details from dicts
        # strings id and comma separated strings ids
        brand_id = str(brands_ids_by_name[item['brand']])
        type_id = str(types_ids_by_name[item['type']])
        magnets_id = str(magnets_ids_by_name[item['magnets']])
        exterior_finishes_ids = ','.join(map(str, [exterior_finishes_ids_by_name[exterior_finish] for exterior_finish in item['exterior_finishes']]))
        plastic_colors_ids = ','.join(map(str, [plastic_colors_ids_by_name[plastic_color] for plastic_color in item['plastic_colors']]))
        interior_plastic_colors_ids = ','.join(map(str, [interior_plastic_colors_ids_by_name[interior_plastic_color] for interior_plastic_color in item['internal_plastic_colors']]))

        writer.add_document(
            id=i,
            name=item['name'],
            short_name=item['short_name'],
            price=item['price'],
            url=item['url'],
            image=item['image'],
            detail_image=item['detail_image'],
            description=item['description'],
            exterior_finishes=exterior_finishes_ids,
            plastic_colors=plastic_colors_ids,
            internal_plastic_colors=interior_plastic_colors_ids,
            brand=brand_id,
            type=type_id,
            magnets=magnets_id,
            size=item['size'],
            weight=item['weight'],
            release_date=item['release_date']
            )

    writer.commit()
    print("###################################")
    print("ITEMS INDEX CREATED")
    print("-----------------------------------")
    print("Number of items: " + str(len(items)))
    print("###################################\n\n")


def load_index_details(details_ixs, details_options):

    brands = details_options['brands']
    types = details_options['types']
    magnets = details_options['magnets']
    exterior_finishes = details_options['exterior_finishes']
    plastic_colors = details_options['plastic_colors']
    internal_plastic_colors = details_options['internal_plastic_colors']

    ix_brands = details_ixs['ix_brands']
    ix_types = details_ixs['ix_types']
    ix_magnets = details_ixs['ix_magnets']
    ix_exterior_finishes = details_ixs['ix_exterior_finishes']
    ix_plastic_colors = details_ixs['ix_plastic_colors']
    ix_interior_plastic_colors = details_ixs['ix_interior_plastic_colors']

    writer = AsyncWriter(ix_brands)
    for i in range(len(brands)):
        brand = brands[i]
        writer.add_document(
            id=i,
            name=brand
        )
    writer.commit()

    writer = AsyncWriter(ix_types)
    for i in range(len(types)):
        type = types[i]
        writer.add_document(
            id=i,
            name=type
        )
    writer.commit()

    writer = AsyncWriter(ix_magnets)
    for i in range(len(magnets)):
        magnet = magnets[i]
        writer.add_document(
            id=i,
            name=magnet
        )
    writer.commit()

    writer = AsyncWriter(ix_exterior_finishes)
    for i in range(len(exterior_finishes)):
        exterior_finish = exterior_finishes[i]
        writer.add_document(
            id=i,
            name=exterior_finish
        )
    writer.commit()

    writer = AsyncWriter(ix_plastic_colors)
    for i in range(len(plastic_colors)):
        plastic_color = plastic_colors[i]
        writer.add_document(
            id=i,
            name=plastic_color
        )
    writer.commit()

    writer = AsyncWriter(ix_interior_plastic_colors)
    for i in range(len(internal_plastic_colors)):
        internal_plastic_color = internal_plastic_colors[i]
        writer.add_document(
            id=i,
            name=internal_plastic_color
        )
    writer.commit()

    print("###################################")
    print("DETAILS INDEX CREATED")
    print("-----------------------------------")
    print("Number of brands: " + str(len(brands)))
    print("Number of types: " + str(len(types)))
    print("Number of magnets: " + str(len(magnets)))
    print("Number of exterior finishes: " + str(len(exterior_finishes)))
    print("Number of plastic colors: " + str(len(plastic_colors)))
    print("Number of internal plastic colors: " + str(len(internal_plastic_colors)))
    print("###################################\n\n")
