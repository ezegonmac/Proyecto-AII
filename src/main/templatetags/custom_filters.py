from django import template

register = template.Library()

# gets a dictionary and a key and returns the value of the key in the dictionary
# used for getting the name of a detail by its id
@register.filter
def get_item(dictionary, key):
    key = int(key) if key.isdigit() else key
    return dictionary.get(key)

# same but for a list of keys
@register.filter
def get_items(dictionary, keys):
    keys = keys.split(',')
    keys = [int(key) for key in keys if key.isdigit()]
    list = [dictionary.get(key) for key in keys]
    return list
