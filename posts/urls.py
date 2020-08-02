"""Posts urls"""
from django.urls import path


from posts import views

urlpatterns = [
    path(
        route='',
        view=views.PostsFeedView.as_view(),
        name="feed"
    ),
    path(
        route='posts/new/',
        view=views.CreatePostView.as_view(),
        name='create'
    ),
    path(
        route='posts/<int:post_id>/',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
]
