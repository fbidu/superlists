"""
Functional tests for the Lists app
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTests


class NewVisitorTest(FunctionalTests):
    """
    Functional tests for a new user
    """

    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        Tests if a client can start a list, add items and
        open it later
        """
        # Edith heard about a cool new online to-do app. She checks the homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute("placeholder"), "Enter a to-do item")

        # She types "Buy 00 Flour" into a text box
        input_box.send_keys("Buy 00 Flour")

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy 00 Flour" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy 00 Flour")

        # There is still a text box inviting her to add another item. She
        # enters "Buy canned tomatoes"
        input_box = self.get_item_input_box()
        input_box.send_keys("Buy canned tomatoes")
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table("1: Buy 00 Flour")
        self.wait_for_row_in_list_table("2: Buy canned tomatoes")

        # Satisfied, she goes back to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys('Buy 00 Flour')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy 00 Flour')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text

        self.assertNotIn("Buy 00 Flour", page_text)
        self.assertNotIn("Buy canned tomatoes", page_text)

        # Francis starts a new list by entering a new item
        input_box = self.get_item_input_box()
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there's no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy 00 Flour", page_text)
        self.assertNotIn("Buy canned tomatoes", page_text)
        self.assertIn("milk", page_text)

        # Satisfied, they both go back to sleep
