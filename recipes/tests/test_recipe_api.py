from unittest.mock import patch

from rest_framework import test

from recipes.tests.test_recipe_base import RecipeAPIMixin


class RecipeAPIv2Test(test.APITestCase, RecipeAPIMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
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
        response = self.get_recipe_api_list()
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
        response_page_1 = self.get_recipe_api_list(query_string='?page=1')
        response_page_2 = self.get_recipe_api_list(query_string='?page=2')
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

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qty=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Create categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Create 10 recipes
        recipes = self.make_recipe_in_batch(qty=10)

        # Change all the recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change 1 recipe to the NOT wanted category
        # As a result, this recipe should be shown in the page.
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        query_string = f'?category_id={category_wanted.id}'
        response = self.get_recipe_api_list(query_string=query_string)

        # We should only see recipes from the wanted category
        self.assertEqual(
            len(response.data.get('results')),
            9  # 10 - 1 = 9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_jwt_login(self):
        print(self.get_jwt_access_token())
