from django.contrib import admin

# Models
from .models import Topic, Room, Message, User

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)
