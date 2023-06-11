from django.shortcuts import render
from . import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def index(request):
    bookmarks = models.Bookmark.objects.filter(author=request.user)
    paginator = Paginator(bookmarks, 5)
    page_number = request.GET.get("page")
    pages = paginator.get_page(page_number)
    return render(request, "index.html", {"bookmarks": bookmarks, "pages": pages})
