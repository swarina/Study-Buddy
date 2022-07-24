from django.forms import ModelForm 

# Models
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    