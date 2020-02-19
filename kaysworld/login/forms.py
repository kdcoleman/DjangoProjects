from django import forms
from django.core import validators

from .models import User
# Create forms here.

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user_exists = User.objects.filter(email=email, password=password).exists()
            if not user_exists:
                self.add_error('password', forms.ValidationError("Incorrect password."))

        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validators.validate_email(email)
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                self.add_error('email', forms.ValidationError("Account not found. Verify the email is correct."))
        except forms.ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

        return email


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', forms.ValidationError("The two password fields didn’t match."))


    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validators.validate_email(email)
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists:
                return email
        except forms.ValidationError:
            raise forms.ValidationError("Enter a valid email address.")
        else:
            raise forms.ValidationError("Sorry, this email is already in use.")

        return email
