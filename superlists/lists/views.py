"""
Module that supplies all the views for the Lists app
"""
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    """
    Renders our simple home_page view and process POST requests
    """
    return render(request, "home.html")


def new_list(request):
    """
    Creates a new list
    """
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})

    return redirect(list_)


def view_list(request, list_id):
    """
    Renders an specific list with all its items
    """
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST["item_text"], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "list.html", {"list": list_, "error": error})
