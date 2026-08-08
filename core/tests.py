from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationTests(TestCase):
    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newtrader',
            'email': 'newtrader@example.com',
            'password1': 'Strong-pass-427!',
            'password2': 'Strong-pass-427!',
        })
        self.assertRedirects(response, reverse('profiles:detail'))
        self.assertTrue(get_user_model().objects.filter(
            username='newtrader').exists())

# Create your tests here.
