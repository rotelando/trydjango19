from django.contrib import admin

# Register your models here.
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp', 'updated']
    list_display_link = ['updated']
    list_filter = ['updated', 'timestamp']
    search_fields = ["title"]

    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
