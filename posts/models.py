from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(verbose_name="Photo de profil", upload_to="profile", blank=True, null=True)


class Theme(models.Model):
    label = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.label


class Post(models.Model):
    title = models.CharField(verbose_name="", max_length=50)
    content = models.TextField(verbose_name="", unique=True)
    illustration = models.ImageField(default=None, blank=True, null=True, upload_to='images/illustrations/%Y/%m/%d/')
    #theme = models.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Theme.ob)
    theme = models.ManyToManyField(Theme, verbose_name="")
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
