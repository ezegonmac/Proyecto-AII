from django.core.paginator import Paginator
from whoosh import index
from whoosh.qparser import MultifieldParser, QueryParser, FuzzyTermPlugin, query

from main.constants import INDEX_FOLDER, INDEX_ITEMS
from main.models import Like


def search_items_index(brand, type, magnets, search, page_number, page_size=20):

    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    # filters query
    if brand == 'Any':
        brand = '*'
    if type == 'Any':
        type = '*'
    if magnets == 'Any':
        magnets = '*'

    brand_query = QueryParser("brand", schema=ix.schema).parse(str(brand))
    type_query = QueryParser("type", schema=ix.schema).parse(str(type))
    magnets_query = QueryParser("magnets", schema=ix.schema).parse(str(magnets))
    filters_query = query.And([brand_query, type_query, magnets_query])

    # search query
    if search == '':
        search = '*'

    if search != '*':
        max_fuzzy_dist = 1
        search = search.replace(' ', f'~{max_fuzzy_dist} ') + f'~{max_fuzzy_dist}'
    search_parser = MultifieldParser(["name", "description"], schema=ix.schema)
    search_parser.add_plugin(FuzzyTermPlugin())
    search_query = search_parser.parse(str(search))

    all_query = query.And([filters_query, search_query])

    items = searcher.search(all_query, limit=None)

    # pagination
    paginator = Paginator(items, page_size)
    page = paginator.get_page(page_number)
    page_items = page.object_list

    num_items = len(items)

    return [page_items, page, num_items]


def search_by_id_index(id):
    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()
    query = QueryParser("id", ix.schema).parse(str(id))
    results = searcher.search(query, limit=None)

    return results[0]


def search_all_index():
    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()
    query = QueryParser("name", ix.schema).parse("*")
    results = searcher.search(query, limit=None)

    return results


def search_all_by_ids_index(items_id):
    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    # Build the query string
    query_string = ""
    for item_id in items_id:
        query_string += f"id:{item_id} OR "
    query_string = query_string[:-4]  # remove the last OR

    # Parse the query string
    query = QueryParser("id", ix.schema).parse(query_string)

    results = searcher.search(query, limit=None)

    return results


def search_all_by_ids_sorted_index(items_id):
    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    results = []
    for item_id in items_id:
        query = QueryParser("id", ix.schema).parse(str(item_id))
        result = searcher.search(query, limit=None)[0]
        results.append(result)

    return results


def search_liked_items_by_user_index(user_id):
    liked_ids = Like.get_items_id_liked_by_user(user_id)
    results = search_all_by_ids_index(liked_ids)

    return results


def search_not_liked_items_by_user_index(user_id):

    items = search_all_index()
    items_ids = [item['id'] for item in items]

    liked_ids = Like.get_items_id_liked_by_user(user_id)
    not_liked_ids = [item_id for item_id in items_ids if item_id not in liked_ids]

    results = search_all_by_ids_index(not_liked_ids)

    return results
