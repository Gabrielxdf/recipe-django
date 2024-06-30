from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.test_recipe_base import RecipeAPIv2Mixin


class RecipeAPIv2Test(test.APITestCase, RecipeAPIv2Mixin):
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
        api_url = self.get_recipe_list_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_acess_token = auth_data.get('jwt_access_token')

        response = self.client.post(
            self.get_recipe_list_reverse_url(),
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}'
        )

        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Arrange (test's config)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')
        jwt_acess_token = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        wanted_new_title = f'The new title updated by {author.username}'

        # Action (test's action)
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={
                'title': wanted_new_title,
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token}'
        )

        # Assertion (test's assertion)
        self.assertEqual(
            response.data.get('title'),
            wanted_new_title,
        )
        self.assertEqual(
            response.status_code,
            200,
        )

    def test_recipe_api_list_logged_user_cant_update_a_recipe_owned_by_another_user(self):  # noqa
        # Arrange (test's config)
        recipe = self.make_recipe()
        access_data = self.get_auth_data(username='test_patch')

        # This user cant update the recipe because it is owned by another user
        another_user = self.get_auth_data(username='cant_update')
        jwt_acess_token_from_another_user = another_user.get(
            'jwt_access_token'
        )

        # This is the actual recipe's owner
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        # Action (test's action)
        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args=(recipe.id,)),
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_acess_token_from_another_user}'
        )

        # Assertion (test's assertion)
        # Another user cant update the recipe, so the status code
        # must be 403 Forbidden
        self.assertEqual(
            response.status_code,
            403,
        )
