from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #Rooms
    path("", views.getRoutes, name="get-routs"),
    path("rooms/", views.getRooms, name="get-rooms"),
    path("rooms/<str:pk>", views.RoomDetails.as_view(), name="get-room"),

    #Topics
    path("topics", views.getTopics, name="topics"),
    path("topics/<str:pk>", views.TopicDetails.as_view(), name="single-topic"),


    #Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]