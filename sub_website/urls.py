from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='website-acceuil'),
    path('submit', views.submit, name='submit'),
    path('substitut/<codebar>', views.substitut, name='substitut'),
    path('substitut_api/<grade>/<codebar>', views.substitut_api, name='substitut_api'),

    path('product/<codebar>', views.product, name='product-page'),
    path('legals', views.legals, name='legals'),
    path('category/<name>', views.category, name='category'),
    path('categories', views.categories, name="categories"),
    path('by_favorites', views.by_favorites, name="by_favorites")
]
