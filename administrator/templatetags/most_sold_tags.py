"""
THIS TEMPLATE TAG IS RESPONSIBLE FOR SHOWING THE MOST SOLD ITEMS ON THE ADMIN HOME PAGE, IT IS BECAUSE IT NEEDS TO ACCESS A DICT IN THE TEMPLATE
"""

from django.template.defaulttags import register


@register.filter
def times_sold(dictionary, key):
    return dictionary.get(key)[0]
  

@register.filter
def revenue(dictionary, key):
    return dictionary.get(key)[1]
