from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    model = Post
    # getting all the 'Published' status posts in date order
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # the template our view will render
    template_name = 'index.html'
    # number of posts per page
    paginate_by = 6
