'''This file will host usefull functions
    that helps our interactions with the database'''
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger

from sub_website.models import Category, Product


def paginate(product_list, paginate_by, current_page):
    '''This function will take in a product list
    paginate it to the number of page wanted and
    return '''

    paginator = Paginator(product_list, paginate_by)

    try:
        list_paginated = paginator.get_page(current_page)
    except PageNotAnInteger:
        list_paginated = paginator.get_page(1)

    return list_paginated


def get_substituts_list(product_to_sub):
    '''This function will take in a product a return a list
    of all avaible substitut within its last categorye.
    If the last cat contains less then 6 products
    the function will look into the fallback category'''

    last_cat = Category.objects.get(name=product_to_sub.last_cat)

    subs_last_cat = last_cat.products.all().filter(grade__lte=product_to_sub.grade).order_by('grade').exclude(codebar=product_to_sub.codebar)
    substitut_list = subs_last_cat

    if len(subs_last_cat) < 6 and product_to_sub.fallback_cat != 'None':
        fallback_cat = Category.objects.get(name=product_to_sub.fallback_cat)
        subs_fallback_cat = fallback_cat.products.all().filter(grade__lte=product_to_sub.grade).order_by('grade').exclude(codebar=product_to_sub.codebar).exclude(codebar__in=subs_last_cat)
        # We can now concatenate the two querryset into one list
        substitut_list = list(chain(subs_last_cat, subs_fallback_cat))

    return substitut_list
