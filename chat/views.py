from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import JsonResponse, HttpResponse

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