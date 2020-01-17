from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import User
from .forms import LoginForm, SignupForm

# Create your views here.

def index(request):
    return render(request, 'login/index.html')


def home(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'login/home.html', {'user': user})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.get(email=email)

            return HttpResponseRedirect(reverse('login:home', args=(user.id,)))

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User(first_name=first_name, last_name=last_name, email=email,
            password=password, join_date=timezone.now())
            user.save()

            return HttpResponseRedirect(reverse('login:home', args=(user.id,)))

    else:
        form = SignupForm()

    return render(request, 'login/signup.html', {'form': form})
