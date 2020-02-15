from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        User = get_user_model()
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("Sorry, this email is already in use.")

        return email


    def get_login_redirect_url(self, request):
        path = "/users/{user_id}/home/"
        return path.format(user_id=request.user.id)


    def get_logout_redirect_url(self, request):
        path = "/users/"
        return path


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        path = "/users/{user_id}/home/"
        return path.format(user_id=request.user.id)
