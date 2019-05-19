from django.urls import path

from . import views

urlpatterns = [
    path('forums/    ', views.ForumListView.as_view(), name='forum_home'),
    path('forums/<int:pk>/', views.TopicListView.as_view(), name='forum_topics'),
    path('forums/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('forums/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_post'),
    path('forums/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('forums/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
]