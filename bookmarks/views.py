from django.shortcuts import render
from . import models
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    bookmarks = models.Bookmark.objects.filter(author=request.user)
    return render(request, 'index.html', {'bookmarks': bookmarks})
