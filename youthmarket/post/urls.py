from django.urls import path, include
from post import views

urlpatterns = [
    path('', views.main, name="main"), # List-All
    path('upload-icon/', views.upload_icon, name="upload_icon"),
    path('detail-icon/<int:icon_id>', views.detail_icon, name="detail_icon"),
    path('create-post/', views.create_post, name='create_post'),
    path('detail-post/<int:post_id>', views.detail_post, name="detail_post"),
    path('my-post/', views.my_post, name="my_post"),
    path('my-detail/', views.my_detail, name="my_detail"),
    path('my-chat-imbuyer/', views.my_chat_imbuyer, name="my_chat_imbuyer"),
    path('my-chat-imseller/', views.my_chat_imseller, name="my_chat_imseller"),
    path('like/', views.like, name="like"),
    path('update-post/<int:post_id>', views.update_post, name="update_post"),
    path('community/', views.community, name="community"),
    path('create-community/', views.create_community, name="create_community"),
    path('detail-community/<int:com_id>', views.detail_community, name="detail_community"),
    path('my-community/', views.my_community, name="my_community"),
]