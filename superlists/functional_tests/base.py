"""
Functional tests for the Lists app
"""
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTests(StaticLiveServerTestCase):
    """
    Base class for functional testing
    """

    def setUp(self):
        """
        setUp starts up our environment before running the tests
        """
        # Defines the browser engine we're going to use
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = f"http://{staging_server}"

        self.browser.implicitly_wait(3)

    def tearDown(self):
        """
        cleans up ou environment after the tests
        """
        # Closes the browser
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """
        Helper function that checks if a text occurs inside
        the id_list_table table
        """
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    # pylint: disable=invalid-name
    def wait_for(self, fn):
        """
        Helper function that waits until a given callable is called
        """
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text):
        """
        waits until a given info appears in the list table
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
