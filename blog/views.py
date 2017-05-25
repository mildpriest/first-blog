from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .models import Post, Comment, Guest
from .porm import PostForm, CommentForm, GuestForm
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.http import HttpResponse


def post_list(request):
    posts = Post.objects.order_by('-created_date')
    return render(request, 'blog/index.html', {'posts': posts})


def ctg_list(request, ctg):
    if ctg == 'py':
        posts = Post.objects.filter(category=1).order_by('-created_date')
    elif ctg == 'java':
        posts = Post.objects.filter(category=2).order_by('-created_date')
    elif ctg == 'javascript':
        posts = Post.objects.filter(category=3).order_by('-created_date')
    return render(request, 'blog/index.html', {'posts': posts})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})


@login_required(login_url='/admin/login/')
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


@login_required(login_url='/admin/login/')
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


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            send_email("provi's blog - 댓글이 등록되었습니다.", "\n작성자 : " + comment.author + "\n내용 : "+ comment.text + "\n\n" + "http://www.provi.xyz/post/" + str(pk))
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def guest(request):
    notes = Guest.objects.order_by('-created_date')

    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            send_email("provi's blog - 방명록이 등록되었습니다.", "\n내용 : " + note.text + "\n\n" + "http://www.provi.xyz/guest/")
            return redirect('guest')
    else:
        form = GuestForm()

    return render(request, 'blog/guest.html', {'form': form, 'notes': notes})


@login_required(login_url='/admin/login/')
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('detail', pk=comment.post.pk)


@login_required(login_url='/admin/login/')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('detail', pk=comment.post.pk)


@login_required(login_url='/admin/login/')
def guest_remove(request, pk):
    note = get_object_or_404(Guest, pk=pk)
    note.delete()
    return redirect('guest')


def send_email(title, text):
    res = send_mail(title, text, "provi.choi@gmail.com", ["provi.choi@gmail.com"], fail_silently=False)
    return HttpResponse(' %s ' % res)
