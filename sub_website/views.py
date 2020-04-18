from django.shortcuts import render
from django.http import Http404

from .logic import functions as f
from .models import Category, Product

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
    results_db_list = Product.objects.filter(name__icontains=value)
    page_number = request.GET.get('page')

    context ={
        'results_db': f.paginate(results_db_list, 6, page_number),
        'paginate': True
    }
    return render(request, 'sub_website/acceuil/results.html', context)

def substitut(request, codebar):
    '''This view will take in a product codebar and return a template
    with all the substituts avaible for said product'''

    page_number = request.GET.get('page')
    try:
        product_searched = Product.objects.get(codebar =codebar)
    except Product.DoesNotExist:
        raise Http404('Le produit recherché n"existe pas')

    aliment = {
        'name' : product_searched.name,
        'grade': product_searched.grade,
        'image': product_searched.image
        } # This dict will be used in our template to display the product we want to substitut
    

    substituts = f.get_substituts_list(product_searched)

    context = {
        'chosen_aliment': aliment,
        'substituts' : f.paginate(substituts, 6, page_number),
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
        'product': product
    }
    return render(request,'sub_website/acceuil/product.html', context)

def legals(request):
    '''This view will display the legals mentions template'''

    return render(request, 'sub_website/acceuil/legals.html')