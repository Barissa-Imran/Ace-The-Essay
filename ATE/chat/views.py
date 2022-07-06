from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def chatView(request):
    return render(request, "chat/chat_home.html")

@login_required
def chatRoomView(request, room_name):
    user = request.user
    context = {
        'room_name': room_name,
        'user': user
    }
    return render(request, "chat/chat_room.html", context)

