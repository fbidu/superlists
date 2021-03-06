"""
Unit tests for the django models.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    """
    Unit tests for the list and item models combined.
    """

    def test_saving_and_retrieving_items(self):
        """
        Tests if we are able to create new lists and items,
        save them and then retrieve all of them.
        """

        # Creating a new list.
        list_ = List()
        list_.save()

        # A new item.
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        # Another new item.
        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        # Getting the saved list.
        saved_list = List.objects.first()
        # Is it the same that we have created?
        self.assertEqual(saved_list, list_)

        # Getting all the items.
        saved_items = Item.objects.all()
        # Are there 2 of them?
        self.assertEqual(saved_items.count(), 2)

        # Checks if the saved items have the same
        # text and list properties as the items
        # we have created in this test.
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        """
        Tests if trying to save an empty
        item raises a ValidationError
        """
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_get_absolute_url(self):
        """
        Tests if a list object is able to compute
        the URL to its representation
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")
