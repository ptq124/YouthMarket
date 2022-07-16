from django import forms
from .models import Icon

class IconForm(forms.Form):
    title = forms.CharField()

class IconModelForm(forms.ModelForm):
    class Meta:
        model = Icon
        fields = ['title', 'photo']
