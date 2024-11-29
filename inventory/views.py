from django.views import generic

from .models import Book


class IndexView(generic.ListView):
    model = Book


class DetailView(generic.DetailView):
    model = Book
