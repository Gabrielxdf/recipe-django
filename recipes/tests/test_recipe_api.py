from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=5)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        # arrange
        wanted_number_of_recipes = 5
        self.make_recipe_in_batch(qty=wanted_number_of_recipes)
        # act
        response = self.client.get(reverse('recipes:recipes-api-list'))
        qty_of_loaded_recipes = len(response.data.get('results'))
        # assert
        self.assertEqual(
            wanted_number_of_recipes,
            qty_of_loaded_recipes
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=3)
    def test_recipe_api_list_is_paginated(self):
        # arrange
        total_number_of_recipes = 5
        recipes_in_page_1 = 3
        recipes_in_page_2 = 2
        self.make_recipe_in_batch(qty=total_number_of_recipes)
        # act
        response_page_1 = self.client.get(
            reverse('recipes:recipes-api-list') + '?page=1'
        )
        response_page_2 = self.client.get(
            reverse('recipes:recipes-api-list') + '?page=2'
        )
        qty_of_loaded_recipes_page_1 = len(response_page_1.data.get('results'))
        qty_of_loaded_recipes_page_2 = len(response_page_2.data.get('results'))
        # assert
        self.assertEqual(
            recipes_in_page_1,
            qty_of_loaded_recipes_page_1
        )
        self.assertEqual(
            recipes_in_page_2,
            qty_of_loaded_recipes_page_2
        )
