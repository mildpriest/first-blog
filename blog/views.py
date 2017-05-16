from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .models import Post
from .porm import PostForm

def post_list(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def ctg_list_py(request):
    posts = Post.objects.filter(category='py').order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def ctg_list_java(request):
    posts = Post.objects.filter(category='java+spring').order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def ctg_list_javascript(request):
    posts = Post.objects.filter(category='javascript').order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/edit.html', {'form': form})

def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'form': form})