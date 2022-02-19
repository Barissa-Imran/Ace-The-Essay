from django.shortcuts import render

def chatView(request):
    return render(request, "chat/chat_home.html")

def chatRoomView(request, room_name):
    context = {
        'room_name': room_name,
    }
    return render(request, "chat/chat_room.html", context)
