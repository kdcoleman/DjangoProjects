from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, 'users/index.html')


def home(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'users/home.html', {'user': user})


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = User.objects.get(email=email_address.email)
    user.email_confirmed = True
    user.save()
