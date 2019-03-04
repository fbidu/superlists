"""
Module that tests our app's forms
"""
from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm


class ItemFormTest(TestCase):
    """
    Tests for the form that manages list items
    """

    def test_form_render_item_text_input(self):
        """
        Is the form being rendered correctly?
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Does the form blocks blank items?
        """
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])
