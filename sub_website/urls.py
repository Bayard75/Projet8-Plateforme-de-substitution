from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='website-acceuil'),
    path('submit', views.submit, name='submit'),
    path('substitut/<codebar>', views.substitut, name='substitut'),
    path('product/<codebar>', views.product, name='product-page'),
    path('legals', views.legals, name='legals')
]
