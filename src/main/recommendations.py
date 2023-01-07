from whoosh import index
from whoosh.query import Every, Or, Term

from main.constants import INDEX_FOLDER, INDEX_ITEMS, ATTRIBUTES_WEIGHTS
from main.models import Like

from whoosh import qparser
from whoosh.scoring import BM25F
from whoosh.sorting import ScoreFacet


def recommend_items(user_id):

    recommended_items = []

    ix = index.open_dir(INDEX_FOLDER, indexname=INDEX_ITEMS)
    searcher = ix.searcher()

    # Get the IDs of the items liked by the user
    liked_item_ids = Like.get_items_id_liked_by_user(user_id)

    # Create a query to match all items
    query = Every()

    # Use the BM25F ranking algorithm to rank the items
    ranking = BM25F(B=0.5, K1=1.5)
    # Create a searcher
    searcher = ix.searcher(weighting=ranking)

    # Search the index for items similar to the liked items
    # scores = ScoreFacet()
    more_like_results = searcher.search(query, limit=None, scored=True)

    print("more_like_results: ", more_like_results)
    for result in more_like_results:
        print("result: ", result, "\n")
        print("score: ", result.score, "\n \n")

    # add recommended items excluding already liked
    for result in more_like_results:
        if result["id"] not in liked_item_ids:
            recommended_items.append(result)

    return recommended_items
