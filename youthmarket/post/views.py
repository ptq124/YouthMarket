from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Icon, User, Post, LikePost, School, ChatRoom, Category, Message, Msg, Community
from .forms import IconModelForm, PostModelForm, CommunityModelForm
import json
from django.utils.safestring import mark_safe

def main(request):
    idx = request.session.get('user') 
    print('main()/idx: ', idx)
    if idx == None:
        return redirect('login')
    print('main()')
    user = get_object_or_404(User, idx=idx)
    print('user.schoolIdx: ', user.schoolIdx) # 홀수고등학교
    # school = get_object_or_404(School, schoolName = str(user.schoolIdx).split('_')[1]) # /홀수고등학교
    school = get_object_or_404(School, schoolName = user.schoolIdx) # 홀수고등학교
    print('scol: ', school)
    posts = Post.objects.exclude(sellerIdx = user).filter(sellerIdx__schoolIdx = school).order_by('-createdDate') #DESC
    # sellers = User.objects.filter(pk=posts.sellerIdx) 판매자이름을 posts에서 접근가능하게 어떻게 할까? 그냥 sellerName을 Post에 넣어버릴까?
    return render(request, 'main_b.html', {'posts': posts, 'user': user})

def detail_post(request, post_id):
    idx = request.session.get('user') 
    print('detail()/idx: ', idx)
    if idx == None:
        return redirect('login')
    post_detail = get_object_or_404(Post, idx = post_id)
    user = get_object_or_404(User, idx = idx)
    try:
        print('detail_post/try')
        like_post = LikePost.objects.get(userIdx = user, postIdx = post_detail)
    except:
        print('detail_post/except')
        like_post = LikePost.objects.create(userIdx = user, postIdx = post_detail)
    like = like_post.like
    if request.method == 'POST':
        print('POST/after like: ', like)
        print('req.body: ', request.body)
        data = json.load(request) # 조건 선택 후 보낸 req
        like = data['like'] # 좋아요: 0 or 1
        print('detail_post/POST/like: ', like)
        like_post.like = like
        like_post.save()
    # post_detail.count += 1
    # post_detail.save()
    print('after like: ', like)
    print(f"post_detail: {post_detail}, post_detail.sellerIdx: {post_detail.sellerIdx}")
    user_object = post_detail.sellerIdx
    print(f'user_object: {user_object}')
    sellerInfo = get_object_or_404(User, idx=user_object.idx)
    print('sellerInfo: ', sellerInfo)
    myInfo = get_object_or_404(User, idx=idx)
    status_code = 200
    multi_idx = ''
    if sellerInfo.idx == myInfo.idx:
        status_code = 201
    else:
        multi_idx = str(post_detail.idx) + '-' + str(sellerInfo.idx) + '-' + str(myInfo.idx)
    print('multi_idx: ', multi_idx)
    print("stauts code",status_code)
    return render(request, 'post_detail_b.html', {'post_detail': post_detail, 'sellerInfo': sellerInfo, 'myInfo': myInfo, 'like': like, 'status_code': status_code})

def create_post(request):
    idx = request.session.get('user') 
    print('crate()/idx: ', idx)
    if idx == None:
        return redirect('login')
    if request.method == "POST" or request.method=="FILES":
        print('create()/POST/if')
        form = PostModelForm(request.POST, request.FILES)
        user = get_object_or_404(User, pk=idx)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.sellerIdx = user
            unfinished.save()
            return redirect('main')
    else:
        print('create()/GET/else')
        form = PostModelForm()
    return render(request, 'post_create_b.html', {'form': form, 'idx': idx})

def my_post(request):
    idx = request.session.get('user') 
    print('my_post()/idx: ', idx)
    if idx == None:
        return redirect('login')
    user_idx = request.session.get('user') # 현재 접속중인 user의 idx를 의미(1: 고경환1, 2: 고경환2)
    posts = Post.objects.filter(sellerIdx = user_idx).order_by('-createdDate') #DESC
    user = get_object_or_404(User, idx = user_idx)
    return render(request, 'my_post_b.html', {'posts': posts, 'user': user})

def my_detail(request):
    idx = request.session.get('user') 
    print('my_detail/idx: ', idx)
    if idx == None:
        return redirect('login')
    user_idx = idx # 현재 접속중인 user의 idx를 의미(1: 고경환1, 2: 고경환2)
    my_info = get_object_or_404(User, idx=user_idx)
    return render(request, 'my_detail_b.html', {'my_info': my_info})

def my_chat_imbuyer(request):
    idx = request.session.get('user') 
    print('my_chat_imbuyer/idx: ', idx)
    if idx == None:
        return redirect('login')
    user_idx = idx
    user = get_object_or_404(User, idx = user_idx)
    chatroom_list = ChatRoom.objects.filter(buyerIdx = user_idx)
    chatroom_info = '' # 1-1-3/2-2-3
    for i in range(len(chatroom_list)):
        print('imseller()/chatroom_list[i]:', chatroom_list[i].postIdx)
        # print('chatroom_list[i].postIdx: ', str(chatroom_list[i].postIdx).split('_')[1])
        # temp_post = get_object_or_404(Post, title=str(chatroom_list[i].postIdx).split('_')[1])
        # temp_seller = get_object_or_404(User, userName=str(chatroom_list[i].sellerIdx).split('_')[1])
        # temp_buyer = get_object_or_404(User, userName=str(chatroom_list[i].buyerIdx).split('_')[1])
        temp_post = get_object_or_404(Post, title=str(chatroom_list[i].postIdx))
        temp_seller = get_object_or_404(User, userName=str(chatroom_list[i].sellerIdx))
        temp_buyer = get_object_or_404(User, userName=str(chatroom_list[i].buyerIdx))
        print('temp_post: ', temp_post)
        print('temp_post.idx: ', temp_post.idx)
        print('temp_seller: ', temp_seller)
        print('temp_seller.idx: ', temp_seller.idx)
        print('temp_buyer: ', temp_buyer)
        print('temp_buyer.idx: ', temp_buyer.idx)
        # print('imseller()/chatroom_list[i]:', chatroom_list[i])
        # print('imseller()/chatroom_lst[i].postIdx: ', chatroom_list[i].postIdx)
        if i == len(chatroom_list)-1:
            chatroom_info += str(temp_post.idx)+ '-' + str(temp_seller.idx) + '-' + str(temp_buyer.idx)
        else:
            chatroom_info += str(temp_post.idx)+ '-' + str(temp_seller.idx) + '-' + str(temp_buyer.idx) + '/'
    print('chatroom_info: ', chatroom_info)
    return render(request, 'my_chatroom_imbuyer.html', {'chatroom_list': chatroom_list, 'user': user, 'chatroom_info': mark_safe(json.dumps(chatroom_info))})

def my_chat_imseller(request):
    idx = request.session.get('user') 
    print('my_chat_imsller/idx: ', idx)
    if idx == None:
        return redirect('login')
    user_idx = idx
    user = get_object_or_404(User, idx = user_idx)
    chatroom_list = ChatRoom.objects.filter(sellerIdx = user_idx)
    # chatroom_list = ChatRoom.objects.filter(buyerIdx = user_idx)
    chatroom_info = '' # 1-1-3/2-2-3
    print('------------------------')
    for i in range(len(chatroom_list)):
        print('imseller()/chatroom_list[i]:', chatroom_list[i].postIdx)
        # print('chatroom_list[i].postIdx: ', str(chatroom_list[i].postIdx).split('_')[1])
        #temp_post = get_object_or_404(Post, title=str(chatroom_list[i].postIdx).split('_')[1])
        #temp_seller = get_object_or_404(User, userName=str(chatroom_list[i].sellerIdx).split('_')[1])
        #temp_buyer = get_object_or_404(User, userName=str(chatroom_list[i].buyerIdx).split('_')[1])
        temp_post = get_object_or_404(Post, title=str(chatroom_list[i].postIdx))
        temp_seller = get_object_or_404(User, userName=str(chatroom_list[i].sellerIdx))
        temp_buyer = get_object_or_404(User, userName=str(chatroom_list[i].buyerIdx))
        print('temp_post: ', temp_post)
        print('temp_post.idx: ', temp_post.idx)
        print('temp_seller: ', temp_seller)
        print('temp_seller.idx: ', temp_seller.idx)
        print('temp_buyer: ', temp_buyer)
        print('temp_buyer.idx: ', temp_buyer.idx)
        # print('imseller()/chatroom_list[i]:', chatroom_list[i])
        # print('imseller()/chatroom_lst[i].postIdx: ', chatroom_list[i].postIdx)
        if i == len(chatroom_list)-1:
            chatroom_info += str(temp_post.idx)+ '-' + str(temp_seller.idx) + '-' + str(temp_buyer.idx)
        else:
            chatroom_info += str(temp_post.idx)+ '-' + str(temp_seller.idx) + '-' + str(temp_buyer.idx) + '/'
    print('chatroom_info: ', chatroom_info)
    return render(request, 'my_chatroom_imseller.html', {'chatroom_list': chatroom_list, 'user': user, 'chatroom_info': mark_safe(json.dumps(chatroom_info))})
def update_post(request, post_id):
    pass
def like(request):
    idx = request.session.get('user') 
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    posts = Post.objects.filter().all()
    post_list = []
    for i in range(len(posts)):
        try:
            like_post = LikePost.objects.get(userIdx = user, like = 1)
            print('like_post.postIdx: ', like_post.postIdx)
            # post = get_object_or_404(Post, title=str(like_post.postIdx).split('_')[1])
            post = get_object_or_404(Post, title=like_post.postIdx)
            print('post: ',post)
            post_list.append(post.idx)
        except:
            continue
    print('post_list: ', post_list)
    post_final_list = Post.objects.filter(idx__in=post_list)
    print('like()/post_lis: ', post_final_list)
    return render(request, 'like.html', {'post_final_list': post_final_list, 'user_info': user})
def like(request):
    idx = request.session.get('user') 
    print('my_chat_imsller/idx: ', idx)
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    posts = Post.objects.filter().all();
    post_list = []
    for i in range(len(posts)):
        try:
            like_post = LikePost.objects.get(userIdx = user, like = 1)
            print('like_post.postIdx: ', like_post.postIdx)
            post = get_object_or_404(Post, title=str(like_post.postIdx).split('_')[1])
            print('post: ',post)
            post_list.append(post.idx)
        except:
            continue
    print('post_list: ', post_list)
    post_final_list = Post.objects.filter(idx__in=post_list)
    print('like()/post_lis: ', post_final_list)
    return render(request, 'like.html', {'post_final_list': post_final_list, 'user_info': user})


# 커뮤니티 생성
def create_community(request):
    idx = request.session.get('user') 
    print('my_chat_imsller/idx: ', idx)
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    if request.method == 'POST':
        form = CommunityModelForm(request.POST)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.userIdx = user
            unfinished.save()
            return redirect('community')
    else:
        form = CommunityModelForm()
    return render(request, 'create_community.html',{'form': form})

# 모든 커뮤니티 랜더링
def community(request):
    idx = request.session.get('user') 
    print('my_chat_imsller/idx: ', idx)
    user = get_object_or_404(User, idx=idx)
    if idx == None:
        return redirect('login')
    communities = Community.objects.filter().order_by('-createdDate') #DESC
    return render(request, 'community.html', {'communities': communities, 'user': user})
    

def detail_community(request, com_id):
    idx = request.session.get('user') 
    print('my_chat_imsller/idx: ', idx)
    user = get_object_or_404(User, idx=idx)
    if idx == None:
        return redirect('login')
    community = get_object_or_404(Community, idx=com_id)
    return render(request, 'detail_community.html', {'community': community, 'user': user})
    

# 커뮤니티 생성
def create_community(request):
    idx = request.session.get('user') 
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    if request.method == 'POST':
        form = CommunityModelForm(request.POST)
        if form.is_valid():
            unfinished = form.save(commit=False)
            unfinished.userIdx = user
            unfinished.save()
            return redirect('community')
    else:
        form = CommunityModelForm()
    return render(request, 'create_community.html', {'form': form})

# 모든 커뮤니티 랜더링
def community(request):
    idx = request.session.get('user') 
    user = get_object_or_404(User, idx=idx)
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    print('user.schoolIdx: ', user.schoolIdx) # 홀수고등학교
    # school = get_object_or_404(School, schoolName = str(user.schoolIdx).split('_')[1]) # 홀수고등학교

    school = get_object_or_404(School, schoolName = user.schoolIdx) # 홀수고등학교

    print('school: ', school)
    communities = Community.objects.exclude(userIdx = user).filter(userIdx__schoolIdx = school).order_by('-createdDate') #DESC
    # communities = Community.objects.filter().order_by('-createdDate') #DESC
    return render(request, 'community.html', {'communities': communities, 'user': user})
    

def detail_community(request, com_id):
    idx = request.session.get('user') 
    user = get_object_or_404(User, idx=idx)
    if idx == None:
        return redirect('login')
    community = get_object_or_404(Community, idx=com_id)
    community.count += 1
    community.save()
    writer = community.userIdx
    return render(request, 'detail_community.html', {'community': community, 'writer': writer})

def my_community(request):
    idx = request.session.get('user') 
    user = get_object_or_404(User, idx=idx)
    if idx == None:
        return redirect('login')
    user = get_object_or_404(User, idx=idx)
    communities = Community.objects.filter(userIdx = user)
    return render(request, 'my_community.html', {'communities': communities, 'user': user})

def school(request):
    if request.method == 'POST':
        print('post/post')
    else:
        print('post/get')
    pass


def upload_icon(request):
    if request.method == 'POST' or request.method == 'FILES':
        form = IconModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # http://127.0.0.1:8000/media/icons/icon_128x128.png
            return redirect('upload_icon')
    else:
        form = IconModelForm()
    return render(request, 'icon_upload.html', {'form': form})

def detail_icon(request, icon_id):
    icon_detail = get_object_or_404(Icon, pk=icon_id)
    return render(request, 'icon_detail.html', {'icon_detail': icon_detail}) # http://127.0.0.1:8000/post/detail/1