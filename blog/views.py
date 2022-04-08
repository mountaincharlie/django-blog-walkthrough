from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm

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
                "commented": False,  # until comments are approved
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
    
    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        # getting the data from the form
        comment_form = CommentForm(data=request.POST)

        # checking if a comment has been made (is True)
        if comment_form.is_valid():
            # getting the users email and username
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # saving the form without commiting
            comment = comment_form.save(commit=False)
            # finding the post the comment was left on
            comment.post = post
            # now saving
            comment.save()
        else:
            comment_form = CommentForm()  # empty instance

        # sending all this info to the render method
        return render(
            request,
            "post_detail.html",  # required template
            # dictionary with the context (data to be passed to template)
            {
                "post": post,
                "comments": comments,
                "commented": True,  # since its been commented on
                "liked": liked,
                "comment_form": CommentForm()
            },
        )
