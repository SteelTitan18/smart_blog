from django import forms
from posts.models import Post
from posts.models import Comment


class PostForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = Post
        fields = ['title', 'content', 'illustration', 'theme']
        widgets = {
            'title' : forms.TextInput(attrs = {'placeholder': 'Titre'}),
            'content' : forms.Textarea(attrs = {'placeholder': 'Contenu'}),
            'theme' : forms.CheckboxSelectMultiple()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs = {'placeholder': 'Commentaire...'})
        }
