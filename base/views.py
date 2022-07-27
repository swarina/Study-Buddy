from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm

# Login
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect.")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

# Logout
def logoutUser(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect('home')

# Register
def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Successfully registered.")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid form data.")

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

# Home Page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

# Room Details  
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

# Create a new Room
@login_required(login_url='login')
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
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if(request.user != room.host):
        return HttpResponse('You are not allowed to update this room!')

    if(request.method == 'POST'):
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# Delete a room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if(request.user != room.host):
        return HttpResponse('You are not allowed to delete this room!')

    if(request.method == 'POST'):
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

# Delete Comment
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if(request.user != message.user):
        return HttpResponse('You are not allowed to delete this message!')

    if(request.method == 'POST'):
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})
