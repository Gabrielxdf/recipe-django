import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_error_not_found_message(self):
        self.browser.get(self.live_server_url)
        # self.sleep(6)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 😢', body.text)
