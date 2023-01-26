from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']