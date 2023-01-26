from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utils import searchProject
from .models import Room, Topic, Message
from .forms import RoomForm, CustomUserCreationForm, UserUpdateForm


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
    rooms, q = searchProject(request)
    rooms_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count, "room_messages":room_messages}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participents.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body"),
        )
        room.participents.add(request.user)
        return redirect("room", pk=room.id)
    context = {"room": room, "room_messages": room_messages, "participants": participants}
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
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {"form": form, "topics":topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room')
        return redirect('home')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {"form": form, "topics":topics, "room":room}
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


@login_required(login_url="login")
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    form = UserUpdateForm(instance=user)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('profile', pk=user.id)
    
    context = {"form": form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activityPage(request):
    messages = Message.objects.all()
    context = {"room_messages": messages}
    return render(request, "base/activity.html", context)
