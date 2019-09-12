"""
Unit tests for the Item Form
"""
from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class ItemFormTest(TestCase):
    """
    Tests for the form that manages list items
    """

    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        Is the form being rendered correctly? With all the required items?
        """
        form = ItemForm()

        # Do we have a placeholder?
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        # Do we use the right css class?
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Does the form blocks blank items?
        """
        form = ItemForm(data={"text": ""})

        # Does the validation fail?
        self.assertFalse(form.is_valid())
        # Do we have an error associated with the empty field?
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        """
        This is a positive test that checks if the form actually works. That
        is, it checks if, given a list and a text, it creates a new item
        and associates that new item is associated with the given list
        """
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me"})
        new_item = form.save(for_list=list_)

        # Do we have a new item?
        self.assertEqual(new_item, Item.objects.first())
        # Did we save the text correctly?
        self.assertEqual(new_item.text, "do me")
        # Did we save it with the correct list?
        self.assertEqual(new_item.list, list_)
