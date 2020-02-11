from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
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
                'password1': '',
                'password2': ''
        }

        form = SignupForm(data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'], ['This field is required.'])
        self.assertEquals(form.errors['last_name'], ['This field is required.'])
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['password1'], ['This field is required.'])
        self.assertEquals(form.errors['password2'], ['This field is required.'])


    def test_signup_form_with_valid_new_user_data(self):
        """
        The signup form is valid when valid data is provided.
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
        The signup form returns an email field error when password1 and password2
        do not match.
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
        The signup form returns an email field error when an email that's already in use
        is provided.
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


class UserLoginFormTests(TestCase):
    def test_blank_login_form(self):
        """
        The login form in invalid when the fields are blank.
        """
        data = {'username': '',
                'password': ''
        }

        form = LoginForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['username'], ['This field is required.'])
        self.assertEquals(form.errors['password'], ['This field is required.'])


    def test_login_form_with_valid_credentials(self):
        """
        The login form is valid when valid credentials are provided.
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
        Form returns a email field error when the incorrect email is provided.
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
        Form returns a password field error when the incorrect password
        is provided.
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
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
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        self.client.login(email=user.email, password='Testing1!')
        response = self.client.get(reverse('login:home', args=(user.id,)))

        self.assertEqual(response.status_code, 200)


    def test_home_view_with_non_authenticated_user(self):
        """
        A user that is not authenticated is redirected to the login page.
        """
        new_user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        response = self.client.get(reverse('login:home', args=(new_user.id,)), follow=True)
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertRedirects(response, '/login/login/?next=/login/{}/home/'.format(new_user.id), status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)


class UserLoginViewTests(TestCase):
    def test_login_view_with_valid_credentials(self):
        """
        Login view redirects to home view with valid credentials.
        """
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
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
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe2@example.com',
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
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
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
                'password1': 'Testing!',
                'password2': 'Testing!'
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
        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'first_name': 'First',
                'last_name': 'Last',
                'email': user.email,
                'password1': 'Testing!',
                'password2': 'Testing!'
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
                'password1': 'Testing!',
                'password2': 'testing!'
        }

        response = self.client.post('/login/signup/', data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')


class UserLogoutViewTests(TestCase):
    def test_user_logout(self):
        """
        Logout view redirects to login view even when user is not logged in.
        """
        response = self.client.get('/login/logout/', follow=True)

        self.assertRedirects(response, reverse('login:login'), status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)


    def test_user_login_and_logout(self):
        """
        Login a user, then logout and redirect to the login view.
        """

        user = User.objects.create_user(first_name='Jane', last_name='Doe',
                    email='janedoe@example.com', password='Testing1!')

        data = {'username': 'janedoe@example.com',
                'password': 'Testing1!'
        }

        self.client.post('/login/login/', data)

        response = self.client.get('/login/logout/', follow=True)

        self.assertRedirects(response, reverse('login:login'), status_code=302, target_status_code=200)
        self.assertEqual(len(response.redirect_chain), 1)
