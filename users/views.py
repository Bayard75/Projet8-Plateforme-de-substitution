from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForme

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
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForme(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Compte mis à jour.')
            return redirect('account')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForme(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/compte.html', context=context)

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
            print(aliment.favorited)
            aliment.favorited += 1
            aliment.save()
            print(aliment.favorited)
        else:
            user.favorites.remove(aliment)
            aliment.favorited -= 1
            aliment.save()
            print(aliment.favorited)

    return redirect('website-acceuil')

@login_required
def show_favorite(request):
    return render(request, 'users/favorites.html')
