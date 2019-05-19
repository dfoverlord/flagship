from rest_framework import serializers

from forums import models


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = {'name', 'description',}
        model = models.Forum
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = {'subject', 'last_updated','forum','creator','views'}
        model = models.Topic
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = {'message', 'topic', 'created_at', 'updated_at', 'created_by', 'updated_by',}
        model = models.Post
