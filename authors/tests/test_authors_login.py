from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsLoginTest(TestCase):
    def test_authors_login_url_is_correct(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_authors_login_url_calls_the_correct_view(self):
        url = reverse('authors:login')
        view = resolve(url)
        self.assertIs(view.func, views.login_view)

    def test_authors_register_view_loads_the_correct_template(self):
        response = self.client.get(reverse('authors:login'))
        self.assertTemplateUsed(response, 'authors/pages/login.html')
