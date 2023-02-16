from rest_framework import serializers
from base.models import Room, Topic, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SingleTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class RoomSerializer(serializers.ModelSerializer):
    host = ProfileSerializer(many=False)
    topic = TopicSerializer(many=False)
    participents = ProfileSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'

