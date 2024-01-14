from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_is_correct(self):
        """Testing if the URL calls the correct view function."""

        view = resolve(reverse('recipes:recipe', args=(1,)))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', args=(1000,))
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_loads_correct_template(self):
        """Testing if the view is rendering the correct template"""

        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It loads one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test if recipe is_published False doesnt show"""

        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)
