from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bookmark

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "url", "description", "read_later", "is_public", "tag_list", "created_at")
    readonly_fields = ("created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(User, UserAdmin)
admin.site.register(Bookmark, BookmarkAdmin)