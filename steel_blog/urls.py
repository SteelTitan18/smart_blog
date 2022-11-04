"""steel_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from posts import views
from django.contrib.auth.models import User
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
# from posts.views import PostListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/', views.home, name="home"),
    path('my_posts/', views.my_posts, name="my-posts"),
    path('sign-in/', views.connexion, name="connexion"),
    path('logout/', views.logout_view, name="logout"),
    path('sign-up/', views.sign_up, name="sign-up"),
    path('Home/add', views.addPost, name="add-post"),
    path('Home/<int:post_id>/', views.DetailPost, name="details"),
    path('Home/<int:post_id>/delete', views.post_delete, name="post-delete"),
    path('Home/<int:post_id>/update/', views.post_update, name="post-update"),
    path('Home/<int:post_id>/like', views.index_like, name="home-like"),
    path('Home/<int:post_id>/dislike', views.index_dislike, name="home-dislike"),
    path('my_posts/<int:post_id>/like', views.my_post_like, name="mypost-like"),
    path('my_posts/<int:post_id>/dislike', views.my_post_dislike, name="mypost-dislike"),
    path('Home/<int:post_id>/detail_like', views.detail_like, name="detail-like"),
    path('Home/<int:post_id>/detail_dislike', views.detail_dislike, name="detail-dislike"),
    path('Home/<int:post_id>/detail_like/<int:comment_id>/', views.comment_like, name="comment-like"),
    path('Home/<int:post_id>/detail_dislike/<int:comment_id>/', views.comment_dislike, name="comment-dislike"),
    path('profile/', views.profile, name="profile"),
    path('profile/modif', views.modif_profile, name="modif-profile")
    # path(r'^post/search$', views.PostSearchListView.as_view(), name='post_search'),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
