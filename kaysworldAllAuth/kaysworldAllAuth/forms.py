from allauth.account.forms import SignupForm, LoginForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.core import validators
from django.utils import timezone
from django import forms
# Create forms here.

class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=200, label='First Name')
    last_name = forms.CharField(max_length=200, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_joined = timezone.now()
        user.save()

        return user

class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})


    def _is_login_email(self, login):
        try:
            validators.validate_email(login)
            ret = True
        except exceptions.ValidationError:
            self.error('login', forms.ValidationError("Enter a valid email address."))
            ret = False
        return ret


    def clean(self):
        super(UserLoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user = get_adapter(self.request).authenticate(
            self.request,
            **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data['login']
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            self.error('password', forms.ValidationError("Incorrect password."))
            raise forms.ValidationError(
                self.error_messages['%s_password_mismatch' % auth_method])
        return self.cleaned_data


class UserSocialSignupForm(SocialSignupForm):
    first_name = forms.CharField(max_length=200, label='First Name')
    last_name = forms.CharField(max_length=200, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(UserSocialSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})


    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_joined = timezone.now()
        user.save()

        return user
