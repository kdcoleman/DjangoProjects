from allauth.account.forms import SignupForm, LoginForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import get_user_model
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
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
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
            self.add_error('login', forms.ValidationError("Enter a valid email address."))
            ret = False
        return ret


    def clean_login(self):
        login = self.cleaned_data.get('login')
        User = get_user_model()
        try:
            User.objects.get(email=login)
        except User.DoesNotExist:
            self.add_error('login', forms.ValidationError("Account not found. Verify the email is correct."))

        return login.strip()


    def clean_password(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')
        User = get_user_model()
        try:
            user = User.objects.get(email=login)
            if not user.check_password(password):
                self.add_error('password', forms.ValidationError("Incorrect Password."))
        except User.DoesNotExist:
            pass

        return password


class UserSocialSignupForm(SocialSignupForm):
    first_name = forms.CharField(max_length=200, label='First Name')
    last_name = forms.CharField(max_length=200, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(UserSocialSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})


    def signup(self, request, user):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.date_joined = timezone.now()
        user.save()

        return user
