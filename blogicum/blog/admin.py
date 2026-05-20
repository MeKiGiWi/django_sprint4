from django.contrib import admin
from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title", "description")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_filter = ("is_published",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "location",
        "image",
        "is_published",
        "pub_date",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = (
        "is_published",
        "author",
        "category",
        "location",
        "pub_date",
    )
    date_hierarchy = "pub_date"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "post", "created_at")
    search_fields = ("text", "author__username", "post__title")
    list_filter = ("created_at", "author")
