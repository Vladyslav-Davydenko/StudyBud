from django.contrib import admin

from .models import Room, Message, Topic

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
