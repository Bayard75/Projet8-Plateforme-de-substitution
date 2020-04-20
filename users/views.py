from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from django.views.decorators.csrf import csrf_exempt
from .models import Profile

from sub_website.models import Product
import json

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte crée, vous pouvez maintenant vous connecter')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/inscription.html', {'form': form})

@login_required
def account(request):
    return render(request, 'users/compte.html')

@csrf_exempt
@login_required
def add_favorite(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        codebar = body['codebar']

        aliment = Product.objects.get(codebar=codebar)
        user = Profile.objects.get(user__email=email)
        if body['action'] == 'add':
            user.favorites.add(aliment)
        else:
            user.favorites.remove(aliment)

    return redirect('website-acceuil')


@login_required
def show_favorite(request):

    return render(request, 'users/favorites.html')
