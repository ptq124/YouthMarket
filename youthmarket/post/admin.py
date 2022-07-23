from django.contrib import admin
from .models import Icon, User, Post, Category, ChatRoom, LikePost, School, Msg, School_User
# Register your models here.
admin.site.register(Icon)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(ChatRoom)
admin.site.register(LikePost)
admin.site.register(School)
admin.site.register(Msg)
admin.site.register(School_User)