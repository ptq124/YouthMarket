# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from post.models import User
import json

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    user_info = get_object_or_404(User, pk=request.session.get('user'))
    userName = user_info.userName
    print('user_info.photo.url: ', user_info.photo.url) # /media/users/kim.jpeg
    return render(request, 'chat_bb.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'userName': mark_safe(json.dumps(userName)),
        'user_photo_url': mark_safe(json.dumps("http://127.0.0.1:8000" + user_info.photo.url))
    })
# def chat(request, post_id):
#     return render(request, 'chat.html', {
#         'chat_room_json': mark_safe(json.dumps(post_id))
#     })
