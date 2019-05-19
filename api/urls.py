from django.urls import path

from . import views


urlpatterns = [
    path('forum/', views.ForumList.as_view(), name='forumlist_api'),
    path('forum/<int:pk>/', views.ForumDetail.as_view(), name='forumdetail_api'),
    path('topic/', views.TopicList.as_view(), name='topiclist_api'),
    path('topic/<int:pk>/', views.TopicDetail.as_view(), name='topicdetail_api'),
    path('post/', views.PostList.as_view(), name='postlist_api'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='postdetail_api'),
]