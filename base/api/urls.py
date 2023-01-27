from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes, name="get-routs"),
    path("rooms", views.getRooms, name="get-rooms"),
    path("rooms/<str:pk>", views.getRoom, name="get-room"),
]