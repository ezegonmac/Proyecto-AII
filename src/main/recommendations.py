from whoosh import index
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import Every

from main.constants import INDEX_FOLDER, INDEX_ITEMS, ATTRIBUTES_FOR_SIMILARITY
from main.models import Like


def recommend_items(user_id):
    # Get a list of the IDs of the items that the user has liked
    liked_items_ids = Like.get_items_id_liked_by_user(user_id)
    if not liked_items_ids:
        # If the user has not liked any items, return an empty list
        return []

    # Initialize an empty list to store the recommended item IDs
    recommended_items = []

    # Iterate through the liked items
    for item_id in liked_items_ids:
        # Get a list of similar items for the current item
        similar_items = get_similar_items(item_id, liked_items_ids)
        # Add the IDs of the similar items to the list of recommended items
        recommended_items.extend(similar_items)

    return recommended_items


def get_similar_items(item_id, liked_items_ids):

    similar_items = []

    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    # # Create a MultifieldParser object that searches across multiple fields
    # parser = MultifieldParser(ATTRIBUTES_FOR_SIMILARITY, schema=ix.schema)
    # # Parse the search query
    # query = Every(ATTRIBUTES_FOR_SIMILARITY)

    parser = MultifieldParser(["name", "description"], schema=ix.schema)
    # Parse the search query
    query = parser.parse("*")  # The query "*" will match all documents in the index

    with ix.searcher() as searcher:

        # Search the index for the item with the given ID
        results = searcher.search(QueryParser("id", schema=ix.schema)
                                    .parse(str(item_id)))

        if not results:
            return []
        else:
            # If the item is found, get the first result (since the ID field is unique, there should only be one result)
            item = results[0]

            # Use the more_like() method to find similar items
            more_like_results = searcher.more_like(item, query, 20)

            # add recommended items excluding already liked
            for result in more_like_results:
                if result["id"] not in liked_items_ids:
                    similar_items.append(result)

    return similar_items
