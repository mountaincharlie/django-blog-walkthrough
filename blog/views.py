from django.shortcuts import render, get_object_or_404
from django.views import generic, View
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


class PostDetail(View):
    # the GET method to get the post from db
    # standard arguments and keyword args
    def get(self, request, slug, *args, **kwargs):
        # getting all the published blogs
        queryset = Post.objects.filter(status=1)
        # getting the post with its slug
        post = get_object_or_404(queryset, slug=slug)
        # getting all the approved comments in date order
        comments = post.comments.filter(approved=True).order_by('created_on')
        # boolean value for if the user liked this post or not
        liked = False
        # checking if the specific user liked it
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # sending all this info to the render method
        return render(
            request,
            "post_detail.html",  # required template
            # dictionary with the context (data to be passed to template)
            {
                "post": post,
                "comments": comments,
                "liked": liked,
            }
        )
