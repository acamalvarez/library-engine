from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Author(models.Model):
    full_name = models.CharField(max_length=123)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    summary = models.TextField()
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    def time_until_available(self):
        borrow_records = self.borrow_set.filter(returned=False).order_by("due_date")
        if not borrow_records:
            return None  # All copies are available
        next_due_date = borrow_records.first().due_date
        return next_due_date - timezone.now()


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    def save(self, *args, **kwargs):
        # Automatically adjust the borrowed_copies count on Book when saving
        if not self.pk:  # If this is a new borrow record
            self.book.available_copies -= 1
            self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        if not self.returned:
            self.returned = True
            self.book.available_copies += 1
            self.book.save()
            self.save()
