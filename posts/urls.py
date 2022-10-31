from django.urls import path

from posts.views.views_post import CreatePostView, PostIndexView

urlpatterns = [
    path('', PostIndexView.as_view(), name='index'),
    path("posts/add", CreatePostView.as_view(), name="add_post"),
]
