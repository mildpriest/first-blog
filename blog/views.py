from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone

from .models import Post, Comment, Guest
from .porm import PostForm, CommentForm, GuestForm

import logging

from pprint import pprint
import json, requests, random, re

logger = logging.getLogger(__name__)

ACCESS_TOKEN = "EAAaBkR9jOPUBAAZBuBPO61JzxC0h8d4fuSYLjZBXoGI5jV3To9tqvL1GZCZBkhJpGqasPWnwb4hYJ3Yih8mrNo5I7ZCZC8b1BJ5MCP94nVCVCeZCYRStrYdOmLaKgUzZBTBliArfbIOTOawlINSVJs17AuERZBWftTFy5WEekhf1mmQZDZD"
FB_IDENTITY = "1282792875171205"


def post_fb_message(fb_id, rec_msg):
    # joke_text = requests.get("http://api.icndb.com/jokes/random/").json()['value']['joke']
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s"%ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fb_id}, "message":{"text":rec_msg}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def post_list(request):
    posts_list = Post.objects.order_by('-created_date')
    paginator = Paginator(posts_list, 4)
    posts = paginator.page(1)

    return render(request, 'blog/index.html', {'posts': posts})


def post_list_page(request, page):
    posts_list = Post.objects.order_by('-created_date')
    paginator = Paginator(posts_list, 4)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts})


def ctg_list(request, ctg):
    if ctg == 'py':
        category_list = Post.objects.filter(category=1).order_by('-created_date')
    elif ctg == 'java':
        category_list = Post.objects.filter(category=2).order_by('-created_date')
    elif ctg == 'javascript':
        category_list = Post.objects.filter(category=3).order_by('-created_date')

    paginator = Paginator(category_list, 4)
    posts = paginator.page(1)

    return render(request, 'blog/index.html', {'posts': posts, 'ctg': ctg})


def ctg_list_page(request, ctg, page):
    if ctg == 'py':
        category_list = Post.objects.filter(category=1).order_by('-created_date')
    elif ctg == 'java':
        category_list = Post.objects.filter(category=2).order_by('-created_date')
    elif ctg == 'javascript':
        category_list = Post.objects.filter(category=3).order_by('-created_date')

    paginator = Paginator(category_list, 4)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts, 'ctg': ctg})


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
            # send_email("provi's blog - 댓글이 등록되었습니다.", "\n작성자 : " + comment.author + "\n내용 : "+ comment.text + "\n\n" + "http://www.provi.xyz/post/" + str(pk))
            # post_fb_message(FB_IDENTITY, "provi's blog - 댓글이 등록되었습니다. ")
            return redirect('detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def guest_page(request, page):
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            # send_email("provi's blog - 방명록이 등록되었습니다.", "\n내용 : " + note.text + "\n\n" + "http://www.provi.xyz/guest/")
            return redirect('guest')
    else:
        form = GuestForm()

    notes_list = Guest.objects.order_by('-created_date')
    paginator = Paginator(notes_list, 10)

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    # logger.error(paginator.num_pages)

    return render(request, 'blog/guest.html', {'form': form, 'notes': notes})


def guest(request):
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            send_email("provi's blog - 방명록이 등록되었습니다.", "\n내용 : " + note.text + "\n\n" + "http://www.provi.xyz/guest/")
            return redirect('guest')
    else:
        form = GuestForm()

    notes_list = Guest.objects.order_by('-created_date')
    paginator = Paginator(notes_list, 10)
    notes = paginator.page(1)

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
