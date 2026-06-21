from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Room, Message, CustomUser
from chat.forms import CustomUserCreationForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def home(request):
    return render(request, 'home.html')


def room(request, room):
    username = request.GET.get('username')
    return render(request, 'room.html', {'username': username, 'room': room})


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    username = request.POST['username']
    room = request.POST['room_id']
    message = request.POST['message']
    new_message = Message.objects.create(value=message, user=username, room=room)
    new_message.save()
    return HttpResponse('Message sent!')


def getMessages(request, room):
    messages = Message.objects.filter(room=room)
    messageList = []
    for msg in messages:
        messageList.append({
            'user': msg.user,
            'value': msg.value,
            'date': str(msg.date),
        })
    return JsonResponse({'messages': messageList})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('login')
            except IntegrityError:
                form.add_error('email', 'This email is already registered.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    return render(request, 'profile.html', {'profile_user': profile_user})