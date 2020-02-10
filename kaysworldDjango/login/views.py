from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import User
from .forms import LoginForm, SignupForm
from .tokens import confirm_account_token

# Create your views here.

def index(request):
    return render(request, 'login/index.html')


def home(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'login/home.html', {'user': user})
    else:
        return HttpResponseRedirect(reverse('login:login'))


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('login:home', args=(user.id,)))
            else:
                return render(request, 'login/login.html', {'form': form})

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login:login'))


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
                send_confirmation_email = False

                if send_confirmation_email:

                    current_site = get_current_site(request)
                    mail_subject = "Confirm your Kay's World account"
                    message = render_to_string('login/confirm.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': confirm_account_token.make_token(user),
                    })
                    to_email = email
                    email_message = EmailMessage(mail_subject, message, to=[to_email])
                    email_message.content_subtype = "html"
                    email_message.send()

                return HttpResponseRedirect(reverse('login:home', args=(user.id,)))

            else:
                return HttpResponse('User is not authenticated!')

    else:
        form = SignupForm()

    return render(request, 'login/signup.html', {'form': form})


def confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and confirm_account_token.check_token(user, token):
        user.email_confirmed = True
        user.save()

        auth_login(request, user)
        return HttpResponseRedirect(reverse('login:home', args=(user.id,)))

    else:
        return HttpResponse('Account confirmation link is invalid!')
