from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Icon(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to='icons') # media/icons에 업로드됨
    def __str__(self):
        return f"{self.id}_{self.title}"

# def upload_user_image(instance):
#     # media/~ 에서 ~에 해당할 값을 return한다
#     return f"/user/{instance.idx}.png"
class School(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    schoolName = models.CharField(max_length=50, verbose_name="학교이름")
    photo = models.ImageField(blank=True, null=True ,upload_to='schools', verbose_name="이미지경로")
    addrCode = models.CharField(max_length=256, verbose_name="우편번호")
    addr = models.CharField(max_length=256, verbose_name="학교주소") 
    detailAddr = models.CharField(max_length=256, verbose_name="상세주소")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성시간") # School row가 생성된 시간
    updatedDate = models.DateTimeField(blank=True, null=True, verbose_name="수정시간") # 수정된 시간
    def __str__(self):
        return f"{self.idx}_{self.schoolName}"
class User(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    schoolIdx = models.ForeignKey(School,to_field="idx", on_delete=models.DO_NOTHING, verbose_name="학교idx")
    userId = models.CharField(max_length=50, null=False, verbose_name="사용자id")
    userPw = models.CharField(max_length=256, null=False ,verbose_name="사용자pw")
    userRePw = models.CharField(max_length=256, null=True, blank=True ,verbose_name="사용자재입력pw")
    userName = models.CharField(max_length=10, null=False, verbose_name="사용자이름")
    photo = models.ImageField(blank=True, null=True ,upload_to='users', verbose_name="이미지경로")
    addrCode = models.CharField(max_length=256, verbose_name="우편번호") # 우편번호
    addr = models.CharField(max_length=256, verbose_name="집 주소") # 집 주소
    detailAddr = models.CharField(max_length=256, verbose_name="상세주소") # 상세주소
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성시간") # 아이디 생성된 시간
    updatedDate = models.DateTimeField(blank=True, null=True, verbose_name="수정시간") # 수정된 시간
    status = models.BooleanField(verbose_name="상태" ,default=False) # 로그인 on/off -> True, False
    def __str__(self):
        return f"{self.idx}_{self.userName}"
# def upload_post_photo(instance):
#     return f"/post/{instance.idx}.png"
class Category(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    category = models.CharField(max_length=10, verbose_name="카테고리명")
    # ex. 가전제품, 식음료
    def __str__(self):
        return str(self.idx)+'_'+str(self.category)

class Post(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    title = models.CharField(max_length=256 ,verbose_name="제목")
    text = models.TextField(verbose_name="내용")
    price = models.CharField(max_length=10, verbose_name="금액")
    sellerIdx = models.ForeignKey(User, to_field="idx", on_delete=models.CASCADE, verbose_name="판매자idx")
    # sellerName = models.ForeignKey(User, to_field="userName", on_delete=models.CASCADE, verbose_name="판매자이름")
    count = models.IntegerField(null=False, default=0, verbose_name="방문자 수")
    photo = models.ImageField(null=True, blank=True, upload_to='posts')
    categoryIdx = models.ForeignKey(Category, to_field="idx", on_delete=models.DO_NOTHING, verbose_name="카테고리idx")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성시간") # 게시글 생성된 시간
    updatedDate = models.DateTimeField(blank=True, null=True, verbose_name="수정시간") # 수정된 시간
    status = models.BooleanField(verbose_name="상태", default=True) # 판매가능 on/off -> True, False
    def __str__(self):
        return f"{self.idx}_{self.title}"

# 없어도 될것같다.
# class PostView(models.Model):
#     postIdx = models.ForeignKey(Post, to_field="idx", on_delete=models.CASCADE)
#     userIdx = models.ForeignKey(User, to_field="idx", on_delete=models.CASCADE)
#     createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성시간") # 아이디 생성된 시간
#     updatedDate = models.DateTimeField(blank=True, null=True, verbose_name="수정시간") # 수정된 시간
#     count = models.IntegerField(verbose_name="방문수") # 판매가능 on/off -> True, False

class ChatRoom(models.Model):
    '''buyerIdx와 sellerIdx의 참조하는 model이 같기때문에 sellerIdx는 IntergerField로 둔다'''
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    postIdx = models.ForeignKey(Post, to_field="idx", on_delete=models.CASCADE, verbose_name="게시글idx")
    buyerIdx = models.ForeignKey(User, to_field="idx", on_delete=models.DO_NOTHING, verbose_name="방만든이idx")
    # makerIdx 로 하면 반대편을 joinerIdx 로 해야되는대 애매하다..
    # 사는 사람이 채팅방을 만들것이므로 buyerIdx로 하겠음.
    # sellerIdx = models.IntegerField(null=False,verbose_name="판매자idx")
    sellerIdx = models.ForeignKey(User, null=True, blank=True, related_name="seller_idx", to_field="idx", on_delete=models.DO_NOTHING, verbose_name="판매자idx")
    # tempIdx = models.ForeignKey(User, null=True, blank=True, related_name="temp_idx" ,to_field="idx", on_delete=models.DO_NOTHING, verbose_name="tempIdx")
    message = models.JSONField(null=True, blank=True, verbose_name="메시지내용")
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="생성시간") # chatRoom 생성된 시간
    updatedDate = models.DateTimeField(blank=True, null=True, verbose_name="수정시간") # 수정된 시간
    status = models.BooleanField(verbose_name="상태", default=True) # 방사용가능 on/off -> True, False
    def __str__(self):
        return f"{self.idx}_{self.buyerIdx}_{self.sellerIdx}"


class LikePost(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    userIdx = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자idx")
    postIdx = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="게시글idx")
    status = models.BooleanField(verbose_name="상태", default=False) # 좋아요 on/off -> True, False
    def __str__(self):
        return f"{self.idx}_{self.userIdx}_{self.postIdx}_{self.status}"

# 테스트용(https://www.youtube.com/watch?v=xrKKRRC518Y)
class Msg(models.Model):
    author = models.ForeignKey(User, related_name="author_messages", on_delete=models.CASCADE, verbose_name="저자")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.userName

    def last_10_messages():
        return Msg.objects.order_by('-timestamp').all()[:10] # ASC

class Message(models.Model):
    idx = models.AutoField(auto_created=True, primary_key=True, verbose_name="idx")
    author = models.ForeignKey(User, related_name="author_message", on_delete=models.CASCADE, verbose_name="저자")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroomIdx = models.ForeignKey(ChatRoom, related_name="chatroom_message", on_delete=models.CASCADE, verbose_name="채팅방idx")
    def __str__(self):
        return self.author.userName

    def last_10_messages(chatroomIdx):
        return Message.objects.filter(chatroomIdx = chatroomIdx).order_by('-timestamp').all()[:10] # ASC