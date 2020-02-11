from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
# Create forms here.

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})


    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                self.add_error('password', forms.ValidationError("Incorrect password."))
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            validate_email(username)
            User.objects.get(email=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Account not found. Verify the email is correct.")
        except forms.ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

        return username


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError("Sorry, this email is already in use.")

        return email
