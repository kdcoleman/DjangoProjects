from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import EmailMessage

from .models import User
from .forms import LoginForm, SignupForm
from .tokens import confirm_account_token

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

            request.session['user_id'] = user.id
            request.session['last_activity'] = str(timezone.now())
            request.session.set_expiry(300)

            return HttpResponseRedirect(reverse('login:home', args=(request.session['user_id'],)))

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

        request.session['user_id'] = user.id
        request.session['last_activity'] = str(timezone.now())
        request.session.set_expiry(300)

        return HttpResponseRedirect(reverse('login:home', args=(request.session['user_id'],)))

    else:
        return HttpResponse('Activation link is invalid!')


def expire_session(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass

    return HttpResponse("Session expired")


def extend_session(request):
    if request.session.get('user_id'):
        request.session['last_activity'] = str(timezone.now())
        return HttpResponse("Session extended")
    else:
        return HttpResponse("Session already expired")
