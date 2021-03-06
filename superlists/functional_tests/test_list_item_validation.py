"""
Functional tests for the Lists app
"""
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTests


class ItemValidationTest(FunctionalTests):
    """
    Class that provides input validation
    """

    def test_cannot_add_empty_list_items(self):
        """
        Tests input validation - empty items are forbidden!
        """
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, because we're using HTML5!
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # She tries again with some text for the item
        self.get_item_input_box().send_keys("Buy milk")

        # and the error message disappears
        self.wait_for(
            lambda: self.browser.find_elements_by_css_selector("#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser blocks her
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:invalid")
        )

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector("#id_text:valid")
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")
