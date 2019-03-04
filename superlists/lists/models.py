"""
Data models for the Lists app
"""
from django.db import models
from django.urls import reverse


class List(models.Model):
    """
    Basic model for our list. Doesn't actually do
    anything besides providing an URL for the list
    and acting as a foreign key for the Item class
    """

    def get_absolute_url(self):
        """
        Returns the URL for the list representation
        """
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    """
    Model for an Item object.
    """

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
