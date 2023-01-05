from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from main.constants import INDEX_FOLDER, INDEX_BRANDS, INDEX_TYPES, INDEX_MAGNETS, INDEX_EXTERIOR_FINISH, INDEX_PLASTIC_COLOR, INDEX_INTERIOR_PLASTIC_COLOR


def get_detail_ids_by_name(index_name):

    ix_brands = open_dir(INDEX_FOLDER, indexname=index_name)
    with ix_brands.searcher() as searcher:
        query = QueryParser("name", ix_brands.schema).parse("*")
        results = searcher.search(query, limit=None)

        details_ids_by_name = {result["name"]: result["id"] for result in results}

    return details_ids_by_name


def get_brands_ids_by_name():
    return get_detail_ids_by_name(INDEX_BRANDS)


def get_types_ids_by_name():
    return get_detail_ids_by_name(INDEX_TYPES)


def get_magnets_ids_by_name():
    return get_detail_ids_by_name(INDEX_MAGNETS)


def get_exterior_finishes_ids_by_name():
    return get_detail_ids_by_name(INDEX_EXTERIOR_FINISH)


def get_plastic_colors_ids_by_name():
    return get_detail_ids_by_name(INDEX_PLASTIC_COLOR)


def get_interior_plastic_colors_ids_by_name():
    return get_detail_ids_by_name(INDEX_INTERIOR_PLASTIC_COLOR)


def get_all_details_ids_by_name():
    return {
        "brands": get_brands_ids_by_name(),
        "types": get_types_ids_by_name(),
        "magnets": get_magnets_ids_by_name(),
        "exterior_finishes": get_exterior_finishes_ids_by_name(),
        "plastic_colors": get_plastic_colors_ids_by_name(),
        "interior_plastic_colors": get_interior_plastic_colors_ids_by_name(),
    }


def get_detail_names_by_id(index_name):

    ix_brands = open_dir(INDEX_FOLDER, indexname=index_name)
    with ix_brands.searcher() as searcher:
        query = QueryParser("name", ix_brands.schema).parse("*")
        results = searcher.search(query, limit=None)

        details_names_by_id = {str(result["id"]): result["name"] for result in results}

    return details_names_by_id


def get_brands_names_by_id():
    return get_detail_names_by_id(INDEX_BRANDS)


def get_types_names_by_id():
    return get_detail_names_by_id(INDEX_TYPES)


def get_magnets_names_by_id():
    return get_detail_names_by_id(INDEX_MAGNETS)


def get_exterior_finishes_names_by_id():
    return get_detail_names_by_id(INDEX_EXTERIOR_FINISH)


def get_plastic_colors_names_by_id():
    return get_detail_names_by_id(INDEX_PLASTIC_COLOR)


def get_interior_plastic_colors_names_by_id():
    return get_detail_names_by_id(INDEX_INTERIOR_PLASTIC_COLOR)


def get_all_details_names_by_id():
    return {
        "brands": get_brands_names_by_id(),
        "types": get_types_names_by_id(),
        "magnets": get_magnets_names_by_id(),
        "exterior_finishes": get_exterior_finishes_names_by_id(),
        "plastic_colors": get_plastic_colors_names_by_id(),
        "interior_plastic_colors": get_interior_plastic_colors_names_by_id(),
    }

