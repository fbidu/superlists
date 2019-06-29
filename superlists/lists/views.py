"""
Module that supplies all the views for the Lists app
"""
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    """
    Renders our simple home_page view and process POST requests
    """
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    """
    Creates a new list
    """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

    return render(request, "home.html", {"form": form})


def view_list(request, list_id):
    """
    Renders an specific list with all its items
    """
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    return render(request, "list.html", {"list": list_, "form": form})
