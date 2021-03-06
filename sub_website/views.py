from django.shortcuts import render
from django.http import Http404

from .logic import functions as f
from .models import Category, Product

import json
from bs4 import BeautifulSoup

import requests


# Create your views here.
def home_page(request):
    '''Function that handles our home page'''
    return render(request, 'sub_website/acceuil/index.html')


def submit(request):
    '''This view will take in a search and return a results
    page with all(or none) of the results from the database'''

    if request.method == 'POST':
        value = request.POST.get('value')
        request.session['value'] = value

    value = request.session['value']
    # We first need to get all the products containg the value searched
    results_list = Product.objects.filter(name__icontains=value)
    page_number = request.GET.get('page')
    from_api = False
    if not results_list:
        results_list = f.get_from_api(value)
        from_api = True
    context = {
        'results_db': f.paginate(results_list, 6, page_number),
        'paginate': True,
        'from_api': from_api,
    }
    return render(request, 'sub_website/acceuil/results.html', context)


def substitut(request, codebar):
    '''This view will take in a product codebar and return a template
    with all the substituts avaible for said product'''

    page_number = request.GET.get('page')
    try:
        product_searched = Product.objects.get(codebar=codebar)
    except Product.DoesNotExist:
        raise Http404("Le produit rechercher non existant")

    aliment = {
        'name': product_searched.name,
        'grade': product_searched.grade,
        'image': product_searched.image
        }  # Dict used in our template for chosen_product

    substituts = f.get_substituts_list(product_searched)

    context = {
        'chosen_aliment': aliment,
        'substituts': f.paginate(substituts, 6, page_number),
        'paginate': True
    }
    return render(request, 'sub_website/acceuil/substitut.html', context)


def substitut_api(request, grade, codebar):
    '''This view will take in a product codebar and return a template
    with all the substituts avaible for said product'''
    page_number = request.GET.get('page')

    r = requests.get(f'https://fr.openfoodfacts.org/produit/{codebar}')
    soup = BeautifulSoup(r.text, 'html.parser')
    image_url = soup.find(id='og_image')['src']
    name = soup.select('span[itemprop=description]')[0].text
    cats = []
    for i in soup.select('a[href*=categorie]'):
        try:
            if 'well_known' in i['class']:
                cats.append(i.text)
        except KeyError:
            pass
    last_cat = cats[-1]
    substituts = f.get_substituts_list(last_cat, api=True, grade=grade,
                                       codebar=codebar)

    aliment = {
        'name': name,
        'image': image_url,
    }
    context = {
        'chosen_aliment': aliment,
        'substituts': f.paginate(substituts, 6, page_number),
        'paginate': True
    }
    return render(request, 'sub_website/acceuil/substitut.html', context)


def product(request, codebar):
    ''' This view will take in a codebar and
    return a template with all revelant information about
    a product'''
    try:
        product = Product.objects.get(codebar=codebar)
    except Product.DoesNotExist:
        raise Http404('Le produit recherchez n"existe pas')

    context = {
        'product': product,
        'stores': json.loads(product.stores)
        }

    return render(request, 'sub_website/acceuil/product.html', context)


def legals(request):
    '''This view will display the legals mentions template'''

    return render(request, 'sub_website/acceuil/legals.html')


def categories(request):
    '''This view will display all categories available in the DB
    by using pagination'''
    page_number = request.GET.get('page')
    categories = Category.objects.all()
    context = {
        "categories": f.paginate(categories, 15, page_number),
        "paginate": True,
    }
    return render(request, 'sub_website/acceuil/categories.html', context)


def by_favorites(request):
    '''This view will display the most favorited product by desceding order'''
    prefered_items = Product.objects.filter(favorited__gte=1).order_by('-favorited')
    context = {
        "prefered": prefered_items,
    }

    return render(request, 'sub_website/acceuil/favorited.html', context)


def category(request, name):
    ''' This view will display all products from a given category'''
    page_number = request.GET.get('page')
    chosen_cat = Category.objects.get(name=name)
    cat_products = chosen_cat.products.all()
    context = {
        'results_db': f.paginate(cat_products, 6, page_number),
        'paginate': True,
    }
    return render(request, 'sub_website/acceuil/results.html', context)
