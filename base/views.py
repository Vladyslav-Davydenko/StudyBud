from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils import searchProject
from .models import Room, Topic, Message
from .forms import RoomForm, CustomUserCreationForm


def loginPage(request):
    page = "login"

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
    context = {"page": page}
    return render(request, "base/login_register.html", context) 


def logoutPage(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('home')


def registerPage(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # commit=False -> freeze object to proces it before saving in DB
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "New User was created")
            login(request, user) 
            return redirect('home')
        else:
            messages.error(request, "An error occured creating a user")

    context ={'page': page, 'form': form }
    return render(request, 'base/login_register.html', context)    


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = searchProject(request)
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count, "room_messages":room_messages}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participents = room.participents.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body"),
        )
        room.participents.add(request.user)
        return redirect("room", pk=room.id)
    context = {"room": room, "room_messages": room_messages, "participents": participents}
    return render(request, "base/room.html", context)


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {"user": user, "rooms": rooms, "room_messages":room_messages, "topics":topics}
    return render(request, "base/profile.html", context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
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
    context = {"obj": room}
    return render(request, "base/delete.html", context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.error(request, 'You are not allowed to delete this message')
        return redirect('home')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {"obj": message}
    return render(request, "base/delete.html", context)
