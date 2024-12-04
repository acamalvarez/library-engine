from django.views import generic

from .models import Book


class IndexView(generic.ListView):
    model = Book

    # def get_queryset(self):
    #     return super().get_queryset().select_related("author")


class DetailView(generic.DetailView):
    model = Book
