from rest_framework import serializers
from base.models import Room, Topic
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    host = ProfileSerializer(many=False)
    topic = TopicSerializer(many=False)
    participents = ProfileSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'