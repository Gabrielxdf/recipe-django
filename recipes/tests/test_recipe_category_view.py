from django.urls import resolve, reverse

from recipes.views import site

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_is_correct(self):
        """Testing if the URL calls the correct view function."""

        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, site.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_loads_correct_template(self):
        """Testing if the view is rendering the correct template"""

        self.make_recipe()
        response = self.client.get(reverse('recipes:category', args=(1,)))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published False doesnt show"""

        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)
