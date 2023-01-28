from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']
        

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'avatar', 'bio']