from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django import forms
from taggit.forms import *
from . import models
from taggit.models import Tag
from django.db.models import Q

class BookmarkForm(forms.Form):
    title = forms.CharField(label="Title", max_length=256)
    url = forms.URLField(label="Url")
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)
    read_later = forms.BooleanField(label="Read Later", required=False)
    is_public = forms.BooleanField(label="Is Public", required=False)
    tags = TagField(required=False)

@login_required
@require_http_methods(['GET'])
def index(request):
    bookmarks = models.Bookmark.objects.filter(author=request.user).order_by("-created_at")
    paginator = Paginator(bookmarks, 20)
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, "index.html", {"bookmarks": pages, "tags": tags})

# javascript:window.location="http://127.0.0.1:8000/bookmarks/add/?url="+encodeURIComponent(document.location)+"&title="+encodeURIComponent(document.title)+"&description="+(document.querySelector(%27meta[name="description"]%27)!=null?document.querySelector(%27meta[name="description"]%27).content:"")+"&tags="+(document.querySelector(%27meta[name="keywords"]%27)!=null?document.querySelector(%27meta[name="keywords"]%27).content:"")@login_required(login_url='/')
@login_required
@require_http_methods(['POST', 'GET'])
def add(request):
    if request.method == "POST":
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = models.Bookmark.objects.create(
                 author=request.user,
                 title=form.cleaned_data['title'],
                 url=form.cleaned_data['url'],
                 description=form.cleaned_data['description'],
                 read_later=form.cleaned_data['read_later'],
                 is_public=form.cleaned_data['is_public'],
            )
            tags = form.cleaned_data['tags']
            for tag in tags:
                bookmark.tags.add(tag)
            return HttpResponseRedirect("/")
    else:
        form = BookmarkForm()
        form.label_suffix = ""
        if request.method == "GET":
            form.fields['title'].initial = request.GET.get('title', '')
            form.fields['url'].initial = request.GET.get('url', '')
            form.fields['description'].initial = request.GET.get('description', '')
    return render(request, 'add.html', {"form": form})

@login_required
@require_http_methods(['DELETE'])
def delete(request, bookmark_id):
    bookmark = get_object_or_404(models.Bookmark, id=bookmark_id, author=request.user)
    bookmark.delete()
    return HttpResponse()

@login_required
@require_http_methods(['POST', 'GET'])
def edit(request, bookmark_id):
    bookmark = get_object_or_404(models.Bookmark, id=bookmark_id, author=request.user)
    if request.method == "POST":
        form = BookmarkForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            bookmark.author=request.user
            bookmark.title=form.cleaned_data['title']
            bookmark.url=form.cleaned_data['url']
            bookmark.description=form.cleaned_data['description']
            bookmark.read_later=form.cleaned_data['read_later']
            bookmark.is_public=form.cleaned_data['is_public']
            tags = form.cleaned_data['tags']
            bookmark.tags.clear()
            for tag in tags:
                bookmark.tags.add(tag)
            bookmark.save()
            print("saved: ", bookmark)
            return HttpResponseRedirect("/")
    else:
        form = BookmarkForm()
        form.label_suffix = ""
        form.fields['title'].initial = bookmark.title
        form.fields['url'].initial = bookmark.url
        form.fields['description'].initial = bookmark.description
        form.fields['tags'].initial = ", ".join(list(bookmark.tags.names()))
    return render(request, 'edit.html', {"form": form, "bookmark_id": bookmark_id})

@login_required
@require_http_methods(['GET'])
def search(request):
    query = request.GET.get("q")
    if query == "":
        bookmarks = models.Bookmark.objects.filter(author=request.user).order_by("-created_at")
        paginator = Paginator(bookmarks, 20)
        page_number = request.GET.get("page")
        pages = paginator.get_page(page_number)
        return render(request, "partials/bookmarks.html", {"bookmarks": pages})
    else:
        bookmarks = models.Bookmark.objects.filter(Q(author=request.user), Q(title__icontains=query) | Q(description__icontains=query))
        paginator = Paginator(bookmarks, 20)
        page_number = request.GET.get("page")
        pages = paginator.get_page(page_number)
    return render(request, "partials/bookmarks.html", {"bookmarks": pages})

@login_required
@require_http_methods(['GET'])
def tag(request, tag_name):
    bookmarks = models.Bookmark.objects.filter(author=request.user, tags__name__in=[tag_name]).order_by("-created_at")
    paginator = Paginator(bookmarks, 20)
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request, "index.html", {"bookmarks": pages, "tags": tags})