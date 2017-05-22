from django import forms

from .models import Post, Comment, Guest


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'text')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('text',)
