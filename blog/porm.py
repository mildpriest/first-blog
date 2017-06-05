from django import forms

from .models import Post, Comment, Guest, FileUpload


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


class FileUpload(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('name', 'file',)

        def __init__(self, *args, **kwargs):   # file 이 없어도 view  >  유효성 검사 시 오류 미발생 적용
            super(PostForm, self).__init__(*args, **kwargs)
            self.fields['file'].required = False