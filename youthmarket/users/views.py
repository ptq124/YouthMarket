from urllib import response
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.handlers import make_password, check_password
from post.models import User, School, School_User
from post.forms import UserModelForm, UserSchoolForm
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
    form = UserModelForm()
    return render(request, 'register.html', {'form': form})

def school(request):
    response_data = {}
    if request.method == 'POST':
        school_name = request.POST.get('school_name', None) # name
        user_name = request.POST.get('user_name', None)
        birthday = request.POST.get('birthday', None)
        phone_number = request.POST.get('phone_number', None)
        print(f'school_name: {school_name}, user_name: {user_name}, birthday: {birthday}, phone_number: {phone_number}')
        if school_name == '홀수고등학교':
            print('school_name_true')
        if user_name == '하현준1':
            print('true22')
        if birthday == '2004-11-07':
            print('true33')
        if phone_number == '010-1111-1111':
            print('true4')
        try:
            print('school()/try')
            # 1_홀수고등학교_010-1111-1111
            # school_user = School_User.objects.get(userName=user_name, birthday=birthday, phone_number=phone_number)
            school_user = School_User.objects.get(userName=user_name)
            print('school_user: ', school_user)
            print('school_name: ', school_name)
            print('type of shcool_name: ', type(school_name))
            print('school_user.schoolIdx: ', school_user.schoolIdx)
            print('type of school_user.schoolIdx: ', type(school_user.schoolIdx))
            ''''''
            if school_name == str(school_user.schoolIdx):
                print('school_name === shco_user.shcoIdx True')
                response_data['status_code'] = 200
                response_data['error'] = '인증이 완료되었습니다.'
            else:
                response_data['status_code'] = 300
            print('out if')
        except:
            print('school()/exception')
            response_data['status_code'] = 300
            response_data['error'] = '학교에 입력한 학생이 존재하지 않습니다.'
    else:
        response_data['status_code'] = 201
    print('response_data: ', response_data)
    print('response_data.get(st_code): ', response_data.get('status_code'))
    return render(request, 'school.html', {'response_data': response_data, 'status_code': response_data.get('status_code')})

def afterschool(request):
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
            else:
                form.save()
            return redirect('login')
    else:
        form = UserModelForm()
        print('afterschool()/GET/form: ', form)
    return render(request, 'afterschool.html', {'form': form})