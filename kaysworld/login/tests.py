from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from django.core import mail
from django.utils import timezone

from .models import User
from .forms import LoginForm, SignupForm

# Create your tests here.

class UserSignupFormTests(TestCase):
    def test_blank_signup_form(self):
        """
        Signup form with no data
        """
        data = {'first_name': '',
                'last_name': '',
                'email': '',
                'password': '',
                'confirm_password': ''
        }

        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'], ['This field is required.'])
        self.assertEquals(form.errors['last_name'], ['This field is required.'])
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['password'], ['This field is required.'])
        self.assertEquals(form.errors['confirm_password'], ['This field is required.'])


    def test_signup_form_with_invalid_email_format(self):
        """
        The signup form returns an email field error when an email that's not in
        email format is provided.
        """

        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'Not an email',
                'password': 'Testing2!',
                'confirm_password': 'Testing2!'
        }

        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Enter a valid email address.'])


    def test_signup_form_with_valid_new_user_data(self):
        """
        The signup form is valid when valid data is provided.
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password': 'Testing!',
                'confirm_password': 'Testing!'
        }

        form = SignupForm(data)

        self.assertTrue(form.is_valid())


    def test_signup_form_with_different_passwords(self):
        """
        The signup form returns an email field error when password1 and password2
        do not match.
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password': 'Testing!',
                'confirm_password': 'testing!'
        }

        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['confirm_password'], ['The two password fields didn’t match.'])


    def test_signup_form_with_taken_email(self):
        """
        The signup form returns an email field error when an email that's already in use
        is provided.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': user.email,
                'password': 'Testing2!',
                'confirm_password': 'Testing2!'
        }

        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Sorry, this email is already in use.'])


class UserLoginFormTests(TestCase):
    def test_blank_login_form(self):
        """
        The login form in invalid when the fields are blank.
        """
        data = {'email': '',
                'password': ''
        }

        form = LoginForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['password'], ['This field is required.'])


    def test_login_form_with_invalid_email_format(self):
        """
        The signup form returns an email field error when an email that's not in
        email format is provided.
        """

        data = {'email': 'Not an email',
                'password': 'Testing1!'
        }

        form = LoginForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Enter a valid email address.'])


    def test_login_form_with_valid_credentials(self):
        """
        The login form is valid when valid credentials are provided.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe@example.com',
                'password': 'Testing1!'
        }

        form = LoginForm(data=data)

        self.assertTrue(form.is_valid())


    def test_login_form_with_incorrect_email(self):
        """
        Form returns a email field error when the incorrect email is provided.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe2@example.com',
                'password': 'Testing1!'
        }

        form = LoginForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'], ['Account not found. Verify the email is correct.'])


    def test_login_form_with_incorrect_password(self):
        """
        Form returns a password field error when the incorrect password
        is provided.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe@example.com',
                'password': 'Testing2!'
        }

        form = LoginForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password'], ['Incorrect password.'])


class UserHomeViewTests(TestCase):
    def test_home_view_with_authenticated_user(self):
        """
        Authenticated user is directed to the home page.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        session = self.client.session
        session['user_id'] = user.id
        session.save()
        response = self.client.get(reverse('login:home', args=(session['user_id'],)))

        self.assertEqual(response.status_code, 200)


    def test_home_view_with_non_authenticated_user(self):
        """
        A user that is not authenticated is redirected to the login page.
        """
        new_user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        new_user.save()

        response = self.client.get(reverse('login:home', args=(new_user.id,)), follow=True)
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertRedirects(response, '/login/login/', status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)


class UserLoginViewTests(TestCase):
    def test_login_view_with_valid_credentials(self):
        """
        Login view redirects to home view with valid credentials.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe@example.com',
                'password': 'Testing1!'
        }

        response = self.client.post('/login/login/', data, follow=True)

        self.assertRedirects(response, reverse('login:home', args=(user.id,)), status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)


    def test_login_view_with_incorrect_email(self):
        """
        When the incorrect email is entered on login form, the form is displayed
        again in the login view with the email field form error.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe2@example.com',
                'password': 'Testing1!'
        }

        response = self.client.post('/login/login/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account not found. Verify the email is correct.')


    def test_login_view_with_incorrect_password(self):
        """
        When the incorrect password is entered on login form, the form is displayed
        again in the login view with the password field form error.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'email': 'janedoe@example.com',
                'password': 'Testing2!'
        }

        response = self.client.post('/login/login/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect password.')


class UserSignupViewTests(TestCase):
    def test_signup_view_with_valid_credentials(self):
        """
        Signup view redirects to home view with valid credentials.
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password': 'Testing!',
                'confirm_password': 'Testing!'
        }

        response = self.client.post('/login/signup/', data, follow=True)
        user = User.objects.get(email='email@example.com')

        self.assertRedirects(response, reverse('login:home', args=(user.id,)), status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)


    def test_signup_view_with_taken_email(self):
        """
        When user enters an email that is already in use, the form is displayed
        again in the signup view with the email field form error.
        """
        user = User(first_name='Jane', last_name='Doe', email='janedoe@example.com',
                    password='Testing1!', join_date=timezone.now())
        user.save()

        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': user.email,
                'password': 'Testing!',
                'confirm_password': 'Testing!'
        }

        response = self.client.post('/login/signup/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sorry, this email is already in use.')


    def test_signup_view_with_different_passwords(self):
        """
        When user enters a different confirmation password, the form is displayed
        again in the signup view with the password field form error.
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password': 'Testing!',
                'confirm_password': 'testing!'
        }

        response = self.client.post('/login/signup/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')


class UserConfirmViewTests(TestCase):
    def test_confirm_email_sent(self):
        """
        Send confirmation email when user signs up. When user clicks on the link
        user.email_confirmed is set to True.
        """
        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': 'email@example.com',
                'password': 'Testing!',
                'confirm_password': 'Testing!'
        }

        response = self.client.post('/login/signup/', data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Confirm your Kay's World account")
