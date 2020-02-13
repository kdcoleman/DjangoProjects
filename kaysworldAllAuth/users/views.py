from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import User
from .forms import LoginForm, SignupForm

# Create your views here.

def index(request):
    return render(request, 'users/index.html')


def home(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'users/home.html', {'user': user})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('users:home', args=(user.id,)))
            else:
                return render(request, 'users/login.html', {'form': form})

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            form.save()
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)

                return HttpResponseRedirect(reverse('users:home', args=(user.id,)))

            else:
                return HttpResponse('User is not authenticated!')

    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})
