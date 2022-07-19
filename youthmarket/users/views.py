from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.handlers import make_password, check_password
from post.models import User
from post.forms import UserModelForm
def login(request):
    response_data = {}
    if request.method == 'POST':
        user_id = request.POST.get('userId', None)
        user_pw = request.POST.get('userPw', None)
        print(f'userId: {user_id}, userPw: {user_pw}')
        if not (user_id and user_pw):
            response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
        else:
            myuser = User.objects.get(userId = user_id)
            if user_pw == myuser.userPw:
                request.session['user'] = myuser.idx # 로그인 세션 유지시킴
                myuser.status = True
                myuser.save()
                print('-------Success login--------')
                return redirect('main')
            
            else:
                response_data['error'] = '비밀번호가 틀렸습니다.'
    else:
        return render(request, 'login.html')
    return render(request, 'login.html', response_data)

def logout(request):
    user = get_object_or_404(User, pk = request.session['user'])
    user.status = False
    user.save()
    request.session.pop('user')
    return redirect('login')

def register(request):
    if request.method == "POST" or request.method == "FILES":
        print('request.method: ', request.method)
        print('request.method.POST: ', request.POST)
        print('request.method.FILES: ', request.FILES)
        print('len of FILES: ', len(request.FILES))
        # 파일이없으면 사용자의 이미지를 기본이미지로 저장
        # http://127.0.0.1:8000/media//icons/user_default.PNG
        form = UserModelForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) == 0:
                unfinished = form.save(commit=False)
                unfinished.photo = "/icons/user_default.PNG" 
                unfinished.save()
            # form.save()
            else:
                form.save()
            return redirect('login')
    else:
        form = UserModelForm()
        print('register()/GET/form: ', form)
    return render(request, 'register.html', {'form': form})

