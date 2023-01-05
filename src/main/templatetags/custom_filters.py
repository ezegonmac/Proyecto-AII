from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_items(dictionary, keys):
    keys = keys.split(',')
    list = [dictionary.get(key) for key in keys]
    if list[0] == None:
        list = []
    return list
