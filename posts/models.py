from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(verbose_name="Photo de profil", upload_to="profile", blank=True, null=True)


class Theme(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.label


class Post(models.Model):
    title = models.CharField(verbose_name="Titre ", max_length=50)
    content = models.TextField(verbose_name="Contenu ", unique=True)
    illustration = models.ImageField(default=None, blank=True, null=True, upload_to='images/illustrations/%Y/%m/%d/')
    theme = models.ForeignKey(Theme, verbose_name="Thème ", on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="liker")
    dislike = models.ManyToManyField(User, related_name="disliker")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    modifHour = models.TimeField(auto_now=True, auto_now_add=False)
    addHour = models.TimeField(auto_now=False, auto_now_add=True)
    modifDate = models.DateField(auto_now=True, auto_now_add=False)
    addDate = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="", unique=True)
    like = models.ManyToManyField(User, related_name="comment_liker")
    dislike = models.ManyToManyField(User, related_name="comment_disliker")
    addHour = models.TimeField(auto_now=True, auto_now_add=False)
    addDate = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.content

# from django.db import models
# from django.contrib.auth.models import User
#
# class Theme(models.Model):
#     label = models.CharField(max_length=30, unique=True)
#
#     def __str__(self):
#         return self.label

# class Post(models.Model):
#     title = models.CharField(verbose_name="Titre ", max_length=50)
#     content = models.TextField(verbose_name="Contenu ", unique=True)
#     theme = models.ForeignKey(Theme, verbose_name="Thème ", on_delete=models.CASCADE)
#     like = models.IntegerField(default=0)
#     dislike = models.IntegerField(default=0)
#     reaction = models.ManyToMayField(User, through='PostReation')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     addHour = models.TimeField(auto_now=True, auto_now_add=False)
#     modifHour = models.TimeField(auto_now=False, auto_now_add=True)
#     addDate = models.DateField(auto_now=True, auto_now_add=False)
#     modifDate = models.DateField(auto_now=False, auto_now_add=True)
#
#     def __str__(self):
#         return self.title
#
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     content = models.TextField(verbose_name="Commentaire ", unique=True)
#     like = models.IntegerField(default=0)
#     dislike = models.IntegerField(default=0)
#     reaction = models.ManyToMayField(User, through='CommentReation')
#     addHour = models.TimeField(auto_now=True, auto_now_add=False)
#     addDate = models.DateField(auto_now=True, auto_now_add=False)
#
#     def __str__(self):
#         return self.content
#
# class PostReaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     dislike = models.BooleanField(default=False)
#
# class CommentReaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Post, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)
#     dislike = models.BooleanField(default=False)
#
