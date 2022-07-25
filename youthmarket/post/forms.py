from dataclasses import field
from attr import fields
from django import forms
from .models import Icon, User, Post, LikePost, School, Community

class IconForm(forms.Form):
    title = forms.CharField()

class IconModelForm(forms.ModelForm):
    class Meta:
        model = Icon
        fields = ['title', 'photo']

class PostForm(forms.Form):
    title = forms.CharField()

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'price','photo', 'categoryIdx']

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['schoolIdx', 'userId', 'userPw', 'userRePw', 'userName', 'photo']
class UserSchoolForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['schoolName', 'userName', 'birthday', 'phoneNumber']
class CommunityModelForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['title', 'text', 'photo']