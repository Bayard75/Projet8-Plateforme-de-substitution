import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sub_project.settings")
application = get_wsgi_application()

import time
import random
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.conf import settings
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from django.db import IntegrityError as CategoryIntegrityError

from sub_website.models import Product, Category
from users.models import Profile

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def create_product(codebar, name, grade):
    'Create a product and a category in our database'
    try:
        test_cat = Category.objects.create(name='test_cat')
    except CategoryIntegrityError:
        test_cat = Category.objects.get(name='test_cat')

    test_product = Product.objects.create(codebar=codebar,
                                          name=name,
                                          grade=grade,
                                          image='https://image.shutterstock.com/image-vector/hand-holding-megaphone-new-product-260nw-387107431.jpg',
                                          reperes='https://static.openfoodfacts.org/images/products/301/762/042/2003/nutrition_fr.146.400.jpg',
                                          last_cat='test_cat',
                                          url='https://www.google.fr/')
    test_product.categories.add(test_cat)
    return test_product

# -------------------------------- Subwebsite APP functional tests ---------------------------- #


class IndexPageSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        self.selenium.implicitly_wait(30)
        self.selenium.maximize_window()

    def tearDown(self):
        self.selenium.quit()

    def test_index_central_form(self):
        # Creating our products to display
        product_names = ['Nutella', 'Bio nutella', 'another nutella product']
        for index, names in enumerate(product_names):
            create_product(index, names, 'b')

        selenium = self.selenium
        product_to_search = Product.objects.filter(name__icontains='nutella')
        selenium.get(self.live_server_url)
        form_input = selenium.find_elements_by_id('input_index')
        submit = selenium.find_element_by_name('submit')

        form_input[0].send_keys('nutella')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        # We check to see if all ouf our elements are indeed there
        for product in product_to_search:
            column = selenium.find_element_by_id(product.codebar)
            name_displayed = column.find_element_by_tag_name('p').text
            self.assertEqual(name_displayed, product.name)

        # The user will click on one of the dispalyed product
        random_product = random.choice(product_to_search)
        element = selenium.find_element_by_id(random_product.codebar)
        # So we make sure that the link is the one expected
        random_product_a_tag = element.find_element_by_tag_name('a')
        self.assertEqual(random_product_a_tag.get_attribute('href'), f"{self.live_server_url}/substitut/{random_product.codebar}")

    def test_index_navbar_form(self):
        # Same test than the previous one but with the nav_bar form

        product_names = ['Nutella', 'Bio nutella', 'another nutella product']
        for index, names in enumerate(product_names):
            create_product(index, names, 'b')

        selenium = self.selenium

        product_to_search = Product.objects.filter(name__icontains='nutella')
        selenium.get(self.live_server_url)

        time.sleep(6)
        form_input = selenium.find_elements_by_id('input_nav_bar')
        submit = selenium.find_element_by_name('submit')

        form_input[0].send_keys('nutella')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)
        # We check to see if all ouf our elements are indeed there
        for product in product_to_search:
            column = selenium.find_element_by_id(product.codebar)
            name_displayed = column.find_element_by_tag_name('p').text
            self.assertEqual(name_displayed, product.name)

        # The user will click on one of the dispalyed product
        random_product = random.choice(product_to_search)
        element = selenium.find_element_by_id(random_product.codebar)
        # So we make sure that the link is the one expected
        random_product_a_tag = element.find_element_by_tag_name('a')
        self.assertEqual(random_product_a_tag.get_attribute('href'), f"{self.live_server_url}/substitut/{random_product.codebar}")

    def test_index_page_no_results(self):
        # Test to see what happends when we have no results in our database
        selenium = self.selenium
        selenium.get(self.live_server_url)
        time.sleep(3)

        form_input = selenium.find_element_by_id('input_index')
        submit = selenium.find_element_by_name('submit')

        form_input.send_keys('nonsense')
        submit.send_keys(Keys.RETURN)
        time.sleep(3)

        no_results = selenium.find_element_by_id('no_results')
        self.assertEqual(no_results.find_element_by_tag_name('h3').text, "NOUS N'AVONS AUCUN PRODUIT CORRESPONDANT À VOTRE RECHERCHE.")


class SubstitutPageSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.selenium.implicitly_wait(30)
        self.selenium.maximize_window()
        substituts = ['sub1', 'sub2', 'sbu3', 'sub4', 'sub5', 'sub6']
        for index, sub in enumerate(substituts):
            create_product(index, sub, 'b')

    def tearDown(self):
        self.selenium.quit()

    def test_page_substitut(self):
        product_to_sub = create_product(8, 'test_product', 'c')
        selenium = self.selenium
        selenium.get(self.live_server_url + f'/substitut/{product_to_sub.codebar}')
        time.sleep(3)

        product_to_sub_displayed = selenium.find_element_by_id("product_to_sub")
        self.assertEqual(product_to_sub_displayed.find_element_by_tag_name('h1').text, product_to_sub.name)

        # The user sees the substituts
        last_cat = Category.objects.get(name='test_cat')
        substituts = last_cat.products.all().filter(grade__lte=product_to_sub.grade).order_by('grade').exclude(codebar=product_to_sub.codebar)
        # Let check that the substituts displayed are correct
        for sub in substituts:
            sub_column = selenium.find_element_by_id(sub.codebar)
            sub_element_a_tag = sub_column.find_element_by_tag_name('a')
            self.assertEqual(sub_element_a_tag.get_attribute('href'),f"{self.live_server_url}/product/{sub.codebar}")
            sub_element_p_tag = sub_column.find_element_by_tag_name('p')
            self.assertEqual(sub_element_p_tag.text, sub.name)
            sub_element_badge = sub_column.find_element_by_tag_name('span')
            self.assertEqual(sub_element_badge.text,sub.grade.upper())

    def test_page_substitut_alreay_best(self):
        product_to_sub = create_product(8, 'test_product', 'a')
        selenium = self.selenium
        selenium.get(self.live_server_url+f'/substitut/{product_to_sub.codebar}')
        time.sleep(3)

        message = selenium.find_element_by_id('message_status')
        message_h2_tag = message.find_element_by_tag_name('h2')
        self.assertEqual(message_h2_tag.text, "Ce produit est déjà le meilleur de sa catégorie")


class ProductPageSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.selenium.implicitly_wait(30)
        self.selenium.maximize_window()

    def tearDown(self):
        self.selenium.quit()

    def test_product_page(self):
        product = create_product(1, 'test_product', 'a')

        selenium = self.selenium
        selenium.get(self.live_server_url + reverse('product-page', args=(product.codebar,)))

        time.sleep(5)
        product_name_h1 = selenium.find_element_by_id('product_name')
        self.assertEqual(product_name_h1.text, product.name)

        product_grade = selenium.find_element_by_id('product_grade')
        self.assertEqual(product_grade.get_attribute('src'), f'https://static.openfoodfacts.org/images/misc/nutriscore-{product.grade}.svg')

        product_reperes = selenium.find_element_by_id('product_reperes')
        self.assertEqual(product_reperes.get_attribute('href'), product.reperes)

        product_url = selenium.find_element_by_id('product_url')
        self.assertEqual(product_url.get_attribute('href'), product.url)


# -------------------------------------------------------------------------------------------- #

# -------------------------------- Users APP functional tests ---------------------------- #
class RegisterPageSeleniumTest(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.selenium.implicitly_wait(30)
        self.selenium.maximize_window()
        
        User.objects.create_user(username='usernameTest',
                                 email='testEmail@gmail.com',
                                 first_name='testFirstname',
                                 last_name='testLastName',
                                 password='test2341')
        user = Profile.objects.get(user__email='testEmail@gmail.com')
        test_product1 = create_product(1, 'test_product1,', 'a')
        test_product2 = create_product(2, 'test_product2,', 'b')
        user.favorites.add(test_product1)
        user.favorites.add(test_product2)

    def tearDown(self):
        self.selenium.quit()
    
    def test_register_page_form(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + reverse('register'))

        username = selenium.find_element_by_name('username')
        email = selenium.find_element_by_name('email')
        password1 = selenium.find_element_by_name('password1')
        password2 = selenium.find_element_by_name('password2')
        submit_btn = selenium.find_element_by_name('submit')
        last_name = selenium.find_element_by_name('last_name')
        first_name = selenium.find_element_by_name('first_name')
        
        username.send_keys('test_user')
        email.send_keys('test_email@gmail.com')
        first_name.send_keys('testFirstname')
        last_name.send_keys('testLastname')
        password1.send_keys('testpassword1')
        password2.send_keys('testpassword1')

        submit_btn.send_keys(Keys.RETURN)

        time.sleep(2)

        self.assertEqual(selenium.current_url, self.live_server_url+reverse('login'))

    def test_account_page_and_login(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + reverse('account'))
        # The user is asked to log in

        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        submit_btn = selenium.find_element_by_name('submit')

        username.send_keys('usernameTest')
        password.send_keys('test2341')
        submit_btn.send_keys(Keys.RETURN)
        time.sleep(2)
        # The user is now on his account page

        name_displayed = selenium.find_element_by_id('username').text
        email_displayed = selenium.find_element_by_id('user_email').text

        self.assertEqual(name_displayed, 'testFirstname')
        self.assertEqual(email_displayed, 'testEmail@gmail.com')

    def test_favorite_page(self):
        selenium = self.selenium
        selenium.get(self.live_server_url + reverse('favorites'))
        # The user is asked to log in and is reddirect to the login page

        username = selenium.find_element_by_name('username')
        password = selenium.find_element_by_name('password')
        submit_btn = selenium.find_element_by_name('submit')

        username.send_keys('usernameTest')
        password.send_keys('test2341')
        submit_btn.send_keys(Keys.RETURN)
        time.sleep(2)

        user = Profile.objects.get(user__email='testEmail@gmail.com')
        for favorite in user.favorites.all():
            div_fav = selenium.find_element_by_id(favorite.name)
            div_fav_a_tag = div_fav.find_element_by_tag_name('a')
            self.assertEqual(div_fav_a_tag.get_attribute('href'), self.live_server_url + reverse('product-page', args=(favorite.codebar,)))

            div_fav_p_tag = div_fav.find_element_by_tag_name('p')
            self.assertEqual(div_fav_p_tag.text, favorite.name)
