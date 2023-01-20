from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils import searchProject
from .models import Room, Topic
from .forms import RoomForm


def loginPage(request):

    if request.user.is_authenticated:
        return redirect("home")


    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            # messages.error(request, 'Username does not exist')
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {}
    return render(request, "base/login_register.html", context) 


def logoutPage(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('home')


def home(request):
    rooms = searchProject(request)
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room')
        return redirect('home')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete this room')
        return redirect('home')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {"room": room}
    return render(request, "base/delete_room.html", context)
