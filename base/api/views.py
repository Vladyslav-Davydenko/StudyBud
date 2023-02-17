from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from base.models import Room, Topic, User
from .serializers import RoomSerializer, TopicSerializer, SingleTopicSerializer, ProfileSerializer
from django.db import IntegrityError

@api_view(['GET'])
def getRoutes(request):
    routes =[
        {"GET": "api/rooms"},
        {"GET": "api/rooms/id"}
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
def getRooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        topic_name = request.data['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)

        rooms = Room.objects.create(
            #host = request.user,

            host = User.objects.get(email=(request.data['host'])),
            topic = topic,
            name = request.data['name'],
            description = request.data['description']
        )
        serializer = serializer = RoomSerializer(rooms, many=False)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class RoomDetails(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return None


    def get(self, request, pk):
        room = self.get_object(pk)
        if not room :
            return Response("Room does not exist")
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)


    def delete(self, request, pk):
        room = self.get_object(pk)
        if not room :
            return Response("Room does not exist")
        room.delete()
        return Response("Room was deleted")

    def patch(self, request, pk):
        room = self.get_object(pk)
        if not room :
            return Response("Room does not exist")
        topic_name = request.data['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.host = User.objects.get(email=request.data["email"])
        room.topic = topic
        room.name = request.data['name']
        room.description = request.data['description']
        room.save()
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def getTopics(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            topic = Topic.objects.create(
                name = request.data['name']
            )
        except IntegrityError:
            return Response("Error this topic already exist")
        serializer = TopicSerializer(topic, many=False)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class TopicDetails(APIView):
    def get_object(self, pk):
        try:
            return Topic.objects.get(id=pk)
        except:
            return None
    
    def get(self, request, pk):
        topic = self.get_object(pk)
        if not topic :
            return Response("Topic does not exist")
        serializer = SingleTopicSerializer(topic, many=False)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        topic = self.get_object(pk)
        if not topic :
            return Response("Topic does not exist")
        topic.name = request.data["name"]   
        topic.save()
        serializer = SingleTopicSerializer(topic, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        topic = self.get_object(pk)
        if not topic :
            return Response("Topic does not exist")
        topic.delete()
        return Response("Room was deleted")


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def addParticipents(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "PUT":
        user = User.objects.get(email=request.data["email"])
        room.participents.add(user)
        room.save()
    serializer = ProfileSerializer(room.participents, many=True)
    return Response(serializer.data)
