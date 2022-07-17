from django import forms
from .models import Icon, User, Post, LikePost, School

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
        fields = ['title', 'text', 'price', 'sellerIdx', 'photo', 'categoryIdx']

