"""sub_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sub_website.urls')),
    path('connexion/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('deconnexion', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('inscription/', user_views.register, name='register'),
    path('compte/', user_views.account, name='account'),
    path('add_fav', user_views.add_favorite, name='add_fav'),
    path('favorites', user_views.show_favorite, name='favorites')
    # Django will only send the string after the path procceed if there's an include
    # Here it will send '' to sub_website.urls
]
