"""
Unit tests for the functions in the list app
"""
import re

from django.http import HttpRequest
from django.shortcuts import render
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape

from lists.forms import ItemForm
from lists.models import Item, List
from lists.views import home_page


def remove_csrf_token(response):
    """
    remove_csrf_token removes the contents of a CSRF token present in a 
    rendered template.

    Those tokens change everytime the page is rendered, so they must be
    extracted before we try to assert that the contents are equal.
    """
    csrf_regex = r"<input[^>]+csrfmiddlewaretoken[^>]+>"
    return re.sub(csrf_regex, "", response.content.decode())


class HomePageTest(TestCase):
    """
    HomePageTest provides a suite of tests for our homepage
    """

    def test_root_url_resolves_to_homepage_view(self):
        """
        Tests if the homepage works!
        """
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        Tests if the home page actually renders the home page
        """
        # Makes a request to our home
        request = HttpRequest()
        response = home_page(request)

        # That request will include an CSRF token. That token changes with each
        # request. We need to remove it in order to be able to test properly
        observed_html = remove_csrf_token(response)

        # We'll have the same problem while rendering the expected response.
        expected_response = render(request, "home.html")
        expected_html = remove_csrf_token(expected_response)

        # Finally, we check everything
        self.assertEqual(observed_html, expected_html)

    def test_home_page_uses_item_form(self):
        """
        Tests if the homepage loads the correct form
        """
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)

class NewListTest(TestCase):
    """
    NewListTest provides tests for creating a new list
    """

    def test_saving_a_post_request(self):
        """
        Tests if a simple POST request is actually saved
        """
        self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        """
        Tests if we're redirected after a POST
        """
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})

        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"item_text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    """
    ListViewTest tests if the rendering and displaying of a created list
    works correctly
    """

    def test_uses_list_template(self):
        """
        Is the list rendered with the correct template?
        """
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        """
        Do we display just the correct list items?
        """
        first_list = List.objects.create()
        Item.objects.create(text="item1", list=first_list)
        Item.objects.create(text="item2", list=first_list)

        second_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=second_list)
        Item.objects.create(text="other list item 2", list=second_list)

        response = self.client.get(f"/lists/{first_list.id}/")

        self.assertContains(response, "item1")
        self.assertContains(response, "item2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self):
        """
        If we have more than one list, are we still rendering the right one?
        """
        # Creating a dummy, empty list
        other_list = List.objects.create()  # pylint: disable=unused-variable
        # Creating the list we want
        correct_list = List.objects.create()
        # Loading the list we want
        response = self.client.get(f"/lists/{correct_list.id}/")

        # Checking if the correct list was sent in the context
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_post_request_to_an_existing_list(self):
        """
        Tests if we can send a post request to an existing list
        and save it. This test was written by me without checking
        the book's solution.
        """
        # Creates a new list
        list_ = List.objects.create()
        # Adds an item to that list
        first_item = Item.objects.create(text="Hai", list=list_)
        # Data regarding a new item we want to add
        new_item = {"item_text": "new item!"}
        # Posts the item
        self.client.post(f"/lists/{list_.id}/", data=new_item)
        # Reading the list
        response = self.client.get(f"/lists/{list_.id}/")

        # This assertion looks more like an functional test than an unit one
        # Notice how in the book's test below, the author did not check
        # for the response contents.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_item["item_text"])
        self.assertContains(response, first_item.text)

    def test_can_save_a_post_request_to_an_existing_list_book(self):
        """
        This is the same test as the above, but as written in the book
        """
        # Creates two lists, to check if we're saving the data in the right one
        other_list = List.objects.create()
        correct_list = List.objects.create()

        # Posts a new item to the correct list
        self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": "A new item!"}
        )

        # Do we have only _one_ item in the database?
        self.assertEqual(Item.objects.count(), 1)
        # Which item is it?
        new_item = Item.objects.first()
        # Is it the one we just sent?
        self.assertEqual(new_item.text, "A new item!")
        # Is it assigned to the correct list?
        self.assertEqual(new_item.list, correct_list)
        # Is the list we didn't touch still empty?
        self.assertEqual(Item.objects.filter(list=other_list).count(), 0)

    def test_post_redirects_to_list_view(self):
        """
        Tests if the correct redirection is being used
        """
        # Again, two lists. One we don't want to change and another one we do
        other_list = List.objects.create()  # pylint: disable=unused-variable
        correct_list = List.objects.create()

        # Creating a new item in the list we do want to change
        response = self.client.post(
            f"/lists/{correct_list.id}/", data={"item_text": "Another item!"}
        )

        # Are we going to be redirect to the correct list?
        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_validation_errors_end_up_on_lists_page(self):
        """
        Checks if validation errors are exposed by the view
        """
        # Create a new list
        list_ = List.objects.create()
        # Adds an invalid item
        response = self.client.post(
            f"/lists/{list_.id}/",
            data={"item_text": ""}
        )

        # Did we have an HTTP-200?
        self.assertEqual(response.status_code, 200)
        # Was the correct template used?
        self.assertTemplateUsed(response, "list.html")
        # The error message we expect to see
        expected_error = escape("You can't have an empty list item")
        # Do we actually see that message?
        self.assertContains(response, expected_error)