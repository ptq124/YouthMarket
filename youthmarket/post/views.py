from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Icon
from .forms import IconModelForm
def index(request):
    return render(request, 'index.html')

def icon_upload(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = IconModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # http://127.0.0.1:8000/media/icons/icon-128x128.png
            return redirect('icon_upload')
    else:
        form = IconModelForm()
    return render(request, 'icon_upload.html', {'form': form})

def icon_detail(request, icon_id):
    icon_detail = get_object_or_404(Icon, pk=icon_id)
    return render(request, 'icon_detail.html', {'icon_detail': icon_detail}) # http://127.0.0.1:8000/post/detail/1
