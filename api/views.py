from django.shortcuts import render
from rest_framework import generics

from forums import views
from forums.models import Post, Topic, Forum
from .serializers import ForumSerializer, TopicSerializer, PostSerializer

# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('created_on')
    serializer_class = PostSerializer
        
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().order_by('created_on')
    serializer_class = PostSerializer


class TopicList(generics.ListCreateAPIView):
    queryset = Topic.objects.all().order_by('last_updated')
    serializer_class = TopicSerializer
    
class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all().order_by('last_updated')
    serializer_class = TopicSerializer
    
    
class ForumList(generics.ListCreateAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    
class ForumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer