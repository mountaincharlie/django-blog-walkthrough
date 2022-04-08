from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        # which table to model it from
        model = Comment
        # the fields we want to have on the form
        fields = ('body',)  # need comma so its treated as Tuple not Str
