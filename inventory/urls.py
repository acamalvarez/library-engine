from django.urls import path

from .views import DetailView, IndexView

 
app_name = "inventory"
urlpatterns = [
    path("", IndexView.as_view(), name="book-list"),
    path("<int:pk>/", DetailView.as_view(), name="book-detail"),
]
