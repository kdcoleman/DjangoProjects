from django.test import TestCase
from .models import User
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate
from django.urls import reverse

# Create your tests here.

class UserFormTests(TestCase):
    def test_signup_form_with_valid_new_user_data(self):
        """
        Sign up new user with valid data
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password1': 'Testing!',
                'password2': 'Testing!'
        }

        form = SignupForm(data)
        self.assertTrue(form.is_valid())


    def test_signup_form_with_different_passwords(self):
        """
        Sign up new user where password1 and password2 do not match
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password1': 'Testing!',
                'password2': 'testing!'
        }

        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'], ['The two password fields didn’t match.'])


    def test_signup_form_with_taken_email(self):
        """
        Sign up new user with an email that's already in use
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': user.email,
                'password1': 'Testing2!',
                'password2': 'Testing2!'
        }

        form = SignupForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Sorry, this email is already in use.'])


    def test_login_form_with_valid_credentials(self):
        """
        Login a user with valid credentials
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
                'password': 'Testing1!'
        }

        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())


    def test_login_form_with_incorrect_email(self):
        """
        Login a user with the incorrect email
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe2@example.com',
                'password': 'Testing1!'
        }

        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['username'], ['Account not found. Verify the email is correct.'])


    def test_login_form_with_incorrect_password(self):
        """
        Login a user with the incorrect password
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
                'password': 'Testing2!'
        }

        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password'], ['Incorrect password.'])
