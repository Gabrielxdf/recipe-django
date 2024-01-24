from django.test import TestCase
from django.urls import resolve, reverse

from authors import views


class AuthorsRegisterTest(TestCase):
    def test_authors_register_url_is_correct(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/register/')

    def test_authors_register_url_calls_the_correct_view(self):
        url = reverse('authors:register')
        view = resolve(url)
        self.assertIs(view.func, views.register_view)

    def test_authors_register_view_loads_the_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/register_view.html')
