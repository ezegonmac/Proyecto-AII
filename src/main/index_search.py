from django.core.paginator import Paginator
from whoosh import index
from whoosh.qparser import MultifieldParser, QueryParser, FuzzyTermPlugin, OperatorsPlugin, query

from main.constants import INDEX_FOLDER, INDEX_ITEMS


def search_items_index(brand, type, search, request, page_size=20):

    if brand == 'Any':
        brand = '*'
    if type == 'Any':
        type = '*'
    if search == '':
        search = '*'

    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    # filters query
    filters_parser = MultifieldParser(["brand", "type"], schema=ix.schema)
    filters_query = filters_parser.parse(f'{brand} {type}')

    # search query
    if search != '*':
        max_fuzzy_dist = 2
        search = search.replace(' ', f'~{max_fuzzy_dist} ') + f'~{max_fuzzy_dist}'
    print(f'search: {search}')
    search_parser = MultifieldParser(["name", "description"], schema=ix.schema)
    search_parser.add_plugin(FuzzyTermPlugin())
    search_query = search_parser.parse(search)

    all_query = query.And([filters_query, search_query])

    items = searcher.search(all_query, limit=None)

    paginator = Paginator(items, page_size)
    page_number = request.GET.get('page')
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
