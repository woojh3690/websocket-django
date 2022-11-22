from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# 메인 페이지
def index(request):
    return render(request, 'chat/index.html')

# 채팅방 페이지
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
