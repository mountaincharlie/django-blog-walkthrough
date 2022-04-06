from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
# creating the blog post status tuple
STATUS = ((0, 'Draft'), (1, 'Published'))


# Post 'table' in our db
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    # related_name => way for you to reffer to it e.g. author.blog_posts
    # on_delete => deleting author deletes all their posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    class Meta:
        # ordering posts by created date (- => descending order)
        ordering = ['-created_on']

    def __str__(self):
        # str representation of how its displayed
        return self.title

    def number_of_likes(self):
        # returns number of likes
        return self.likes.count()


# Comments 'table' in our db
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        # str representation of how its displayed
        return f"Comment {self.body} by {self.name}"
