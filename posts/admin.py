from django.contrib import admin
from posts.models import Post
from posts.models import Theme
from posts.models import Comment
from posts.models import User

class UserAdmin(admin.ModelAdmin):
    list_diplay = ("image", "username", "last_name", "first_name", "username", "email", "password")

class PostAdmin(admin.ModelAdmin):
    list_diplay = ("title", "content", "theme")

class ThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "label")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "post", "user")

admin.site.register(Post, PostAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
