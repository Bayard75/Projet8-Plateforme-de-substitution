import requests

from django.core.management.base import BaseCommand
from django.db import IntegrityError as CategoryIntegrityError
from django.db.utils import IntegrityError as ProductIntegrityError

from sub_website.models import Category, Product


class Command(BaseCommand):

    help = 'Populate our database with categories and Products'

    def populate_aliment(self):
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
                        # Deleting withespace to avoid duplacate

                    aliment = Product.objects.create(
                        codebar=product['code'],
                        name=product['product_name_fr'],
                        grade=product['nutrition_grade_fr'],
                        url=product['url'],
                        reperes=product['image_nutrition_url'],
                        image=product['image_front_url'],
                        last_cat=cat_list[-1]
                        # Will be used to find a substitut later
                    )

                    if len(cat_list) > 1:
                        # If we have more than 1 cat we can add a fallback cat
                        aliment.fallback_cat = cat_list[-2]
                        aliment.save()

                    print('Aliment suivant ajouté : ',
                          product['product_name_fr'])

                    for cat in cat_list:
                        try:
                            category_to_create = Category.objects.create(name=cat)
                            aliment.categories.add(category_to_create)
                            print('Category suivante ajouté : ', cat)

                        except CategoryIntegrityError:
                            # If the Category as already been created
                            print('La category suivante est déjà inserée : ', cat)
                            category_to_add = Category.objects.get(name=cat)
                            aliment.categories.add(category_to_add)


                except ProductIntegrityError:
                    # If a product with the same name is present in the database we go to the next one
                    print('Un aliment de ce nom est déjà present : ',
                          product['product_name_fr'])
                    pass

                except KeyError:
                    # In case a product doesn't have all the releveant information we go the next one
                    pass
            print('page : ', page)
            page += 1

    def handle(self, *args, **options):
        self.populate_aliment()

p = "Yaourt sucrés,Yaourt sucré"
a = p.split(',')
for b, c in enumerate(a):
    a[b] = c.strip()

print(a)