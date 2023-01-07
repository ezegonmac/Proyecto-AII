from main.constants import ATTRIBUTES_WEIGHTS
from main.index_search import search_all_by_ids_sorted_index, search_liked_items_by_user_index, search_not_liked_items_by_user_index


def recommend_items(user_id):

    liked_items = search_liked_items_by_user_index(user_id)
    not_liked_items = search_not_liked_items_by_user_index(user_id)

    scores = compute_scores(liked_items, not_liked_items)

    recommended_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    recommended_items_ids = [item for item, score in recommended_scores]

    recommended_items = search_all_by_ids_sorted_index(recommended_items_ids)

    return recommended_items


def compute_scores(liked_items, not_liked_items):
    scores = {item["id"]: 0 for item in not_liked_items}

    for item in not_liked_items:
        item_score = 0
        for liked_item in liked_items:
            item_score += item_similarity(liked_item, item)
        scores[item["id"]] = item_score

    return scores


def item_similarity(liked_item, item):

    similarities = attributes_similarity(liked_item, item)

    similarity = 0
    for attribute, sim in similarities.items():
        weight = ATTRIBUTES_WEIGHTS[attribute]
        similarity += weight * sim

    # normalize
    similarity /= len(similarities)

    return similarity

def attributes_similarity(liked_item, item):
    similarities = {}

    if "short_name" in liked_item and "short_name" in item:
        short_name_sim = dice_coefficient(set(liked_item["short_name"]), set(item["short_name"]))
        similarities["short_name"] = short_name_sim

    # every sim is 1 if the attribute is the same, 0 otherwise
    if "brand" in liked_item and "brand" in item:
        brand_sim = 1 if liked_item["brand"] == item["brand"] else 0
        similarities["brand"] = brand_sim
    if "type" in liked_item and "type" in item:
        type_sim = 1 if liked_item["type"] == item["type"] else 0
        similarities["type"] = type_sim
    if "magnets" in liked_item and "magnets" in item:
        magnets_sim = 1 if liked_item["magnets"] == item["magnets"] else 0
        similarities["magnets"] = magnets_sim
    if "weight" in liked_item and "weight" in item:
        weight_sim = 1 if liked_item["weight"] == item["weight"] else 0
        similarities["weight"] = weight_sim
    if "size" in liked_item and "size" in item:
        size_sim = 1 if liked_item["size"] == item["size"] else 0
        similarities["size"] = size_sim

    # every sim between 0 and 1
    if "exterior_finishes" in liked_item and "exterior_finishes" in item:
        exterior_finishes_sim = list_attribute_similarity(liked_item["exterior_finishes"], item["exterior_finishes"])
        if exterior_finishes_sim is not None:
            similarities["exterior_finishes"] = exterior_finishes_sim
    if "plastic_colors" in liked_item and "plastic_colors" in item:
        plastic_colors_sim = list_attribute_similarity(liked_item["plastic_colors"], item["plastic_colors"])
        if plastic_colors_sim is not None:
            similarities["plastic_colors"] = plastic_colors_sim
    if "internal_plastic_colors" in liked_item and "internal_plastic_colors" in item:
        internal_plastic_colors_sim = list_attribute_similarity(liked_item["internal_plastic_colors"], item["internal_plastic_colors"])
        if internal_plastic_colors_sim is not None:
            similarities["internal_plastic_colors"] = internal_plastic_colors_sim

    return similarities


def list_attribute_similarity(liked_attribute, item_attribute):
    if liked_attribute is None or item_attribute is None:
        return None
    if len(liked_attribute) == 0 or len(item_attribute) == 0:
        return None

    matching_attributes = 0
    for a in liked_attribute:
        if a in item_attribute:
            matching_attributes += 1

    return matching_attributes / len(liked_attribute)


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))
