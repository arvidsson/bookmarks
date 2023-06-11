from django.shortcuts import render
from . import models

def index(request):
    bookmarks = models.Bookmark.objects.filter(author=request.user)
    return render(request, 'index.html', {'bookmarks': bookmarks})
