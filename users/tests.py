from django.test import TestCase
from django.contrib.auth.models import User

from django.urls import reverse

from .forms import UserRegisterForm, LoginForm
from .models import Profile
from sub_website.models import Product


import json
# Create your tests here.


class RegisterPageTestCase(TestCase):
    # This view should return a page if the method is get
    # Or create a new user and redirect to the login page

    def test_register_page_return_200(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_new_user(self):
        username = 'usernameTest'
        email = 'testEmail@gmail.com'
        password1 = 'test2341'
        password2 = 'test2341'

        response = self.client.post(reverse('register'),
                                    {
                                        'username': username,
                                        'email': email,
                                        'password1': password1,
                                        'password2': password2
                                    })

        user = User.objects.get(email=email)
        self.assertIsNotNone(user)
        self.assertRedirects(response, reverse('login'))


class AccountPageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='usernameTest',
                                             email='testEmail@gmail.com',
                                             password='test2341')

    def test_login_return_200(self):
        self.client.login(username='usernameTest', password='test2341')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_login_redirects(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, reverse('login')+'?next=/compte/')


class AddFavoriteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='usernameTest',
                                             email='testEmail@gmail.com',
                                             password='test2341')
        self.user_profile = Profile.objects.get(user__email=self.user.email)

        self.test_product = Product.objects.create(codebar='1',
                                                   name='test_product')

    def test_add_favorite_redirects_not_authentificated(self):
        response = self.client.get(reverse('add_fav'))
        self.assertRedirects(response, reverse('login')+'?next=/add_fav')

    def test_add_favorite_redirects_get_authentificated(self):
        self.client.login(username='usernameTest', password='test2341')
        response = self.client.get(reverse('add_fav'))
        self.assertRedirects(response, reverse('website-acceuil'))

    def test_adding_favorite(self):
        self.client.login(username='usernameTest', password='test2341')
        body = {'email': self.user.email,
                'codebar': '1',
                'action': 'add'}

        response = self.client.post(reverse('add_fav'),
                                    json.dumps(body),
                                    content_type='application/json')
        favorite = self.user_profile.favorites.get(codebar='1')
        self.assertIsNotNone(favorite)

    def test_remove_favorite(self):

        self.client.login(username='usernameTest', password='test2341')
        self.user_profile.favorites.add(self.test_product)

        body = {'email': self.user.email,
                'codebar': self.test_product.codebar,
                'action': 'delete'}

        response = self.client.post(reverse('add_fav'),
                                    json.dumps(body),
                                    content_type='application/json')

        self.assertFalse(self.user.profile.favorites.filter(codebar=self.test_product.codebar).exists())


class ShowFavoritePageTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='usernameTest',
                                             email='testEmail@gmail.com',
                                             password='test2341')

    def test_show_favorite_redicts_noauthentifacted(self):
        response = self.client.get(reverse('favorites'))
        self.assertRedirects(response, reverse('login')+'?next=/favorites')

    def test_show_favorite_return_200(self):
        self.client.login(username='usernameTest', password='test2341')

        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
