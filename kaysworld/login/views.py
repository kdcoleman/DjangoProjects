from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import User
from .forms import LoginForm, SignupForm

# Create your views here.

def index(request):
    try:
        del request.session['user_id']
        request.session.flush()
    except KeyError:
        pass
    return render(request, 'login/index.html')


def home(request, user_id):
    if request.session.get('user_id'):
        user = get_object_or_404(User, pk=request.session.get('user_id'))
        return render(request, 'login/home.html', {'user': user})
    else:
        return HttpResponseRedirect(reverse('login:login'))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)

            if user.password == password:
                request.session['user_id'] = user.id
                request.session['last_activity'] = str(timezone.now())
                request.session.set_expiry(300)
                return HttpResponseRedirect(reverse('login:home', args=(request.session['user_id'],)))
            else:
                return render(request, 'login/login.html', {'form': form})

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

            request.session['user_id'] = user.id
            request.session['last_activity'] = str(timezone.now())
            request.session.set_expiry(300)

            return HttpResponseRedirect(reverse('login:home', args=(request.session['user_id'],)))

    else:
        form = SignupForm()

    return render(request, 'login/signup.html', {'form': form})


def extend_session(request):
    if request.session.get('user_id'):
        request.session['last_activity'] = str(timezone.now())
        return HttpResponse("Session extended")
    else:
        return HttpResponseRedirect(reverse('login:login'))
