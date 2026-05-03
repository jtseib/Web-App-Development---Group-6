from django import template

register = template.Library()

@register.filter(name="get_item")
@register.filter(name="dict_get")
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)
