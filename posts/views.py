from django.shortcuts import render
from posts.forms import PostForm
from posts.forms import CommentForm
from django.shortcuts import redirect
from posts.models import User
from django.contrib.auth import authenticate, login, logout
from posts.models import Post
from posts.models import Comment
from posts.models import Theme
from django.contrib.auth.decorators import login_required
import django.views.generic as gnr
from django.views.generic.edit import CreateView
from django.contrib import messages
from PIL import Image
from django.core.paginator import Paginator
# import operator
# from functools import reduce
# from django.views.generic.list import ListView
# from django.db.models import Q

def home(request):
    postDic = {}
    _postList = Post.objects.all().order_by('modifDate').reverse()
    paginator = Paginator(_postList, 5)
    number = request.GET.get('page')
    postList = paginator.get_page(number)
    themes = Theme.objects.all()
    posts = []

    if request.method == "GET":
        _request = request.GET.get('_request')
        if _request is not None:
            postList = list(Post.objects.filter(title__icontains = _request))
            for th in themes:
                if _request.lower() == th.label.lower():
                    posts = list(Post.objects.filter(theme = th))
            for post in posts:
                if post not in postList:
                    postList.append(post)

    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        postDic[_post] = (comment)
    addPost(request)

    # return redirect('home')

    return render(request, 'posts/index.html', {'postD':postDic, 'themes':themes, 'result':_request, 'page_obj': postList})

# class PostListView(gnr.ListView):
#     template_name = 'posts/index.html'
#
#     def get(self, request):
#         postDic = {}
#         queryset = Post.objects.all()
#         for _post in queryset:
#             comment = Comment.objects.filter(post = _post).count()
#             postDic[_post] = (comment)
#         return render(request, self.template_name, {'postDic':postDic})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('connexion')
    return render(request, 'posts/login.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
        passw = request.POST['password']
        user = User.objects.create_user(username, mail, passw)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if request.FILES['profile_image'] != None:
            user.image = request.FILES['profile_image']
        user.save()
        return redirect('home')

    return render(request, 'posts/sign_up.html')

@login_required(login_url='/sign-in/')
def addPost(request):
    request.POST._mutable = True
    # messages.add_message(request, messages.INFO,"Vous devez être connecté !")
    if request.method == 'POST':
        post = Post()
        post.user = request.user
        # post.title = request.POST['title']
        # post.theme = Theme.objects.get(label=request.POST['theme'])
        # post.content = request.POST['content']
        # post.save()
        form = PostForm(request.POST, request.FILES, instance=post)
        if request.POST["theme"] == "" and request.POST["new_theme"] != "":
            theme = Theme()
            theme.label = request.POST["new_theme"]
            theme.save()
            request.POST["theme"] = theme
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'posts/addPost.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def DetailPost(request, post_id):
    _post = Post.objects.get(id = post_id)
    url = _post.illustration.name
    comments = Comment.objects.filter(post = _post)
    my_post = []
    if request.user.is_authenticated:
        my_post = Post.objects.filter(user = request.user)

    if request.method == 'POST':
        comment = Comment()
        if request.user.is_authenticated:
            comment.user = request.user
            comment.post = Post.objects.get(id = post_id)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save()
                return redirect("details", post_id)
        else:
            messages.add_message(request, messages.INFO,"Vous devez être connecté !")
            return redirect("connexion")
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': _post, 'comments':comments, 'my_post':my_post, 'form':form, 'len':len(comments), 'name':url})

def my_posts(request):
    postDic = {}
    _postList = Post.objects.filter(user = request.user).order_by('modifDate').reverse()
    # _postList = Post.objects.all().order_by('modifDate').reverse()
    paginator = Paginator(_postList, 5)
    number = request.GET.get('page')
    postList = paginator.get_page(number)
    themes = Theme.objects.all()

    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        postDic[_post] = (comment)
    addPost(request)
    return render(request, 'posts/my_posts.html', {'postD':postDic, 'themes':themes, 'page_obj': postList})

def profile(request):
    return render(request, 'posts/user_profile.html')

def modif_profile(request):
    redirection = 'profile'
    if request.method == 'POST':
        user = request.user
        pseudo = user.username
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        if request.FILES['profile_image'] != None:
            user.image = request.FILES['profile_image']
        if user == authenticate(username = pseudo, password = request.POST['old_password']):
            user.set_password(request.POST['new_password'])
            redirection = 'connexion'
        user.save()

        return redirect('connexion')

    return render(request, 'posts/modif_profile.html')

# def modif_profile(request):
#     user = User.objects.get(id = user_id)
#
#     if request.method == 'POST':
#         form =

def post_delete(request, post_id):
    post = Post.objects.get(id = post_id)
    post.delete()
    return redirect('my-posts')

    return render(request, 'listings/my_posts.html', {'post':post})

def post_update(request, post_id):
    post = Post.objects.get(id = post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('details', post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_update.html', {'form':form})

@login_required(login_url='/sign-in/')
def index_like(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.like.all():
        post.like.add(request.user)
    else:
        post.like.remove(request.user)
    if request.user in post.dislike.all():
        post.dislike.remove(request.user)
    post.save()

    return redirect('home')

@login_required(login_url='/sign-in/')
def index_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.dislike.all():
        post.dislike.add(request.user)
    else:
        post.dislike.remove(request.user)
    if request.user in post.like.all():
        post.like.remove(request.user)
    post.save()

    return redirect('home')

@login_required(login_url='/sign-in/')
def detail_like(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.like.all():
        post.like.add(request.user)
    else:
        post.like.remove(request.user)
    if request.user in post.dislike.all():
        post.dislike.remove(request.user)
    post.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def detail_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.dislike.all():
        post.dislike.add(request.user)
    else:
        post.dislike.remove(request.user)
    if request.user in post.like.all():
        post.like.remove(request.user)
    post.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def my_post_like(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.like.all():
        post.like.add(request.user)
    else:
        post.like.remove(request.user)
    if request.user in post.dislike.all():
        post.dislike.remove(request.user)
    post.save()

    return redirect('my-posts')

@login_required(login_url='/sign-in/')
def my_post_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.user not in post.dislike.all():
        post.dislike.add(request.user)
    else:
        post.dislike.remove(request.user)
    if request.user in post.like.all():
        post.like.remove(request.user)
    post.save()

    return redirect('my-posts')

@login_required(login_url='/sign-in/')
def comment_like(request, post_id, comment_id):
    post = Post.objects.get(id = post_id)
    comment = Comment.objects.get(id = comment_id)
    if request.user not in comment.like.all():
        comment.like.add(request.user)
    else:
        comment.like.remove(request.user)
    if request.user in comment.dislike.all():
        comment.dislike.remove(request.user)
    comment.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def comment_dislike(request, post_id, comment_id):
    post = Post.objects.get(id = post_id)
    comment = Comment.objects.get(id = comment_id)
    if request.user not in comment.dislike.all():
        comment.dislike.add(request.user)
    else:
        comment.dislike.remove(request.user)
    if request.user in comment.like.all():
        comment.like.remove(request.user)
    comment.save()

    return redirect('details', post.id)

# class PostSearchListView(ListView):
#     model = Post
#     context_object_name = "post_lst"
#     template_name = "posts/index.html"
#     paginate_by = 10
#
#     def get_queryset(self):
#         result = super(PostSearchListView, self).get_queryset()
#
#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )
#
#         return result

# class DetailPost(gnr.DetailView):
#     template_name = 'posts/post_detail.html'
#     model = Post

# @login_required(login_url='/sign-in/')
# def Commenting(request, post_id):
#
#     # comment = Comment()
#     # comment.user = request.user
#     # comment.post = Post.objects.get(id = post_id)
#     if request.method == 'POST':
#         print("okk")
#
#         comment = Comment()
#         comment.user = request.user
#         comment.post = Post.objects.get(id = post_id)
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             return redirect("details", post_id)
#     else:
#         form = CommentForm()
#     return render(request, 'posts/comment.html', {'form':form})

# class Commenting(CreateView):
#     template_name = 'posts/comment.html'
#     model = Comment
#     fields = ['content']
#     success_url = 'details'
#
#     # @login_required(login_url='/sign-in/')
#     def post(self, request, pk):
#         comment = Comment()
#         comment.user = self.request.user
#         comment.post = Post.objects.get(id = pk)
#         form = CommentForm(instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             return redirect('details')
#         else:
#             form = CommentForm(instance=comment)
#         return render(request, self.template_name, {'form':form})
