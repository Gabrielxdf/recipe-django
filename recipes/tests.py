from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeURLsTest(TestCase):
    # Testing if urls is correct

    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        # sent named arguments in a dict
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        # sent the args in order in a tuple
        url = reverse('recipes:recipe', args=(1,))
        self.assertEqual(url, '/recipes/1/')


class RecipeViewsTest(TestCase):
    # Testing if the url is calling the correct view
    ...

    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)


class RecipeTemplatesTest(TestCase):
    # Testing if the view is rendering the correct template
    ...
