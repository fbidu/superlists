"""
Functional tests for the Lists app
"""
from .base import FunctionalTests


class LayoutAndStylingTest(FunctionalTests):
    """
    Class for testing layout
    """

    def test_layout_and_styling(self):
        """
        Basic test for centering
        """
        # Edith heard about a cool new online to-do app. She checks the homepage.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location["x"] + input_box.size["width"] / 2, 512, delta=5
        )
