from . import views
from django.urls import path

urlpatterns = [
    # url (no extension) uses PostList class view and its the homepage
    path('', views.PostList.as_view(), name='home'),
]