from django.test import TestCase,LiveServerTestCase
from django.urls import reverse

from .models import Product, Category
from .logic import functions as f
# Create your tests here.


'''         Models Tests             '''
    
class ProductModelTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            codebar='1',
            name='test_product',
            grade='a',
            url='www.test_url.com',
            reperes='www.reperes.com',
            image='www.image.com',
            last_cat='last_cat'
        )
    
    def test_product_created(self):
        self.assertTrue(Product.objects.filter(codebar='1').exists())
    
    def test_data_product_exact(self):
        self.assertEqual(self.product.name, 'test_product')
        self.assertEqual(self.product.grade, 'a')
        self.assertEqual(self.product.url, 'www.test_url.com')
        self.assertEqual(self.product.reperes, 'www.reperes.com')
        self.assertEqual(self.product.image, 'www.image.com')
        self.assertEqual(self.product.last_cat, 'last_cat')

class CategoryModelTestCase(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='test_cat')
    
    def test_category_created(self):
        self.assertTrue(Category.objects.filter(name='test_cat').exists())

    def test_data_category_exact(self):
        self.assertEqual(self.category.name,'test_cat')

class ProductCategoryInteractionTestCase(TestCase):
    
    def setUp(self):
        self.product =  self.product = Product.objects.create(
                        codebar='1',
                        name='test_product',
                        grade='a',
                        url='www.test_url.com',
                        reperes='www.reperes.com',
                        image='www.image.com',
                        last_cat='last_cat')
        self.category = Category.objects.create(name='test_cat')
    
    def test_adding_category_to_product(self):
        self.product.categories.add(self.category)
        self.assertIn(self.category,self.product.categories.all())
        
    
'''         Views Tests             '''


class HomePageTestCase(TestCase):
    # Home_page
        # Return 200 
    def test_home_page(self):
        response = self.client.get(reverse('website-acceuil'))
        self.assertEqual(response.status_code, 200)

class SubmitPageTestCase(TestCase):
    
    # Submit
    def test_submit_page_return_200(self):
        response = self.client.post(reverse('submit'),{'value':'test'})
        self.assertEqual(response.status_code,200)

class SubstitutPageTestCase(TestCase):
    # Substitut
    def test_substitut_page_return_200(self):
        #Return 200 if we get a querryset
        Product.objects.create(codebar='2', name='test',grade='e',last_cat='lastcat')
        Category.objects.create(name='lastcat')
        response = self.client.get(reverse('substitut',args=('2',)))
        self.assertEqual(response.status_code, 200)
    
    def test_substitut_page_return_404(self):
        # Return 404 if product we want to substitut doesn't exist

        response = self.client.get(reverse('substitut', args=('2')))
        self.assertEqual(response.status_code, 404)

class ProductPageTestCase(TestCase):
    # Product
    def test_product_page_return_200(self):
        # Return 200 if product exist
        Product.objects.create(codebar='2', name='test')
        response = self.client.get(reverse('product-page',args=('2',)))
        self.assertEqual(response.status_code, 200)
    
    def test_product_page_return_404(self):
        # Return 404 if product doesn't exist

        response = self.client.get(reverse('product-page', args=('2',)))
        self.assertEqual(response.status_code, 404)

class PaginateFunctionTestCase(TestCase):

    def test_paginate_return_populated_list(self):
        product_list = ['Product1','Product2','Product3','Product4','Product5']
        list_paginated = f.paginate(product_list,2,1)
        self.assertGreater(len(list_paginated), 0)
    
    def test_paginate_return_empty_list(self):
        product_list = []
        list_paginated = f.paginate(product_list,2,1)
        self.assertEqual(len(list_paginated), 0)


'''             functional tests        '''
