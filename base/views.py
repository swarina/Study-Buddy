from django.shortcuts import render, redirect

# Models
from .models import Room
from .forms import RoomForm

# Home Page
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

# Room Details  
def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room': room}
    return render(request, 'base/room.html', context)

# Create a new Room
def createRoom(request):
    form = RoomForm()
    
    if(request.method == 'POST'):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# Update a room
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if(request.method == 'POST'):
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# Delete a room
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if(request.method == 'POST'):
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})
