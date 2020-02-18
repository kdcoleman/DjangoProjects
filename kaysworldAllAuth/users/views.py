from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from allauth.account.models import EmailAddress
from django.utils import timezone
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, 'users/index.html')


def home(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        email = get_object_or_404(EmailAddress, user=request.user)
        return render(request, 'users/home.html', {'user': user, 'email': email})
