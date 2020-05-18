import requests

from django.core.management.base import BaseCommand
from django.db import IntegrityError as CategoryIntegrityError
from django.db.utils import IntegrityError as ProductIntegrityError

from sub_website.models import Category, Product


class Command(BaseCommand):

    help = 'Populate our database with categories and Products'

    def update_databse(self):
        '''This function will populate our database with aliment
        from the OpenfoodFacts API'''

        page = 1  # Starting at page 1
        nb_aliments_to_display = 4000
        while Product.objects.count() < nb_aliments_to_display:

            search_url = f'https://fr.openfoodfacts.org/cgi/search.pl?search_terms=&search_simple=1&action=process&page={page}&json=True'
            response = requests.get(search_url)
            data = response.json()

            for product in data['products']:
                try:
                    cat_list = product['categories'].split(',')
                    # We put all the Product categories into a list
                    for index, sentence in enumerate(cat_list):
                        cat_list[index] = sentence.strip()
                    
                    aliment, created = Product.objects.update_or_create(
                        codebar = product['code'],
                        name= product['product_name_fr'],
                        defaults={
                                'grade': product['nutrition_grade_fr'],
                                'url': product['url'],
                                'reperes': product['image_nutrition_url'],
                                'image': product['image_front_url'],
                                'last_cat':cat_list[-1]}
                    )
                
                    if created:
                        print("L'aliment suivant à été crée : ", product['product_name_fr'])
                    else:
                        print("L'aliment suivant à été updaté : ", product['product_name_fr'])

                    if len(cat_list) > 1:
                        # If we have more than 1 cat we can add a fallback cat
                        aliment.fallback_cat = cat_list[-2]
                        aliment.save()

                    for cat in cat_list:
                        try:
                            category_to_create = Category.objects.create(name=cat)
                            aliment.categories.add(category_to_create)

                        except CategoryIntegrityError:
                            category_to_add = Category.objects.get(name=cat)
                            aliment.categories.add(category_to_add)   

                except ProductIntegrityError:
                    pass
                except KeyError:
                    # In case a product doesn't have all the releveant information we go the next one
                    pass
            print('page : ', page)
            page += 1
 

    def handle(self, *args, **options):
        self.update_databse()
