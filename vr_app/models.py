from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ms_app.models import Library

class HelpData(models.Model):
    question_title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    question_content = models.TextField()
    question_visit = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return self.question_title
    def summary(self):
        return self.body[:100]
    def update_counter(self):		
        self.question_visit = self.question_visit + 1
        self.save()

class Comment(models.Model):
    question = models.ForeignKey(HelpData,on_delete= models.CASCADE, null=True,related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_contents = models.CharField(max_length=200)
    class Meta:
        ordering =['-id']
    def __str__(self):
        return self.comment_contents


# ohjinjin 08/03/19 AM 02:54 커스텀된 유저 모델이 중복되어버려서 문제가 생긴건지 잘 나오질않아여...ㅜㅜ 확인후에 이어서 작업하겠습니다
# https://gyukebox.github.io/blog/django-%EC%84%A4%EC%A0%95-%EB%8D%94%EC%9A%B1-%EC%84%B8%EB%B6%80%EC%A0%81%EC%9C%BC%EB%A1%9C-%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0/
# ohjinjin, 08/03/19 AM 01:39 defined profile class
class Profile2(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  #id,pw,email, firstname, lastname
    test_record = models.FileField(upload_to = 'musics/',blank=True)
    sex = models.CharField(max_length=15, blank=True)
    birth_date = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15,blank=True)
    agreement1 = models.CharField(max_length=10, blank=True)
    agreement2 = models.CharField(max_length=10, blank=True)
    mileage = models.CharField(max_length=10, default=0, blank=True)
    realmile = models.CharField(max_length=10, default =0, blank=True)
"""class Apply(models.Model):ohjinjin 080619 PM15:08
    writer = models.CharField(max_length=150) # username
    pub_date = models.DateField()
    library_id = models.IntegerField()  # Library table 내 primary key
    1365_id = models.charFiels(max_length = 30) # 1365 ID 테이블 추가했어요(손현준)
    """

###### apply model 수정 8_8 찬호 ######
class Apply(models.Model): #ohjinjin 080619 PM15:08
    primarykey = models.OneToOneField(Library, on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    """writer = models.CharField(max_length=150) # username  -   id 
    date = models.DateTimeField('date published')
    vms_1365_id = models.CharField(max_length = 30) # 1365 ID 테이블 추가했어요(손현준)
    privacy = models.CharField(max_length = 150)
    BookPermission = models.IntegerField(max_length=10,default = 0,blank =True)
    writer_name = models.CharField(max_length=150) # 작성자 이름 
    sms = models.BooleanField(default=False)"""
    vms_or_1365 = models.CharField(max_length=10,blank=True)
    vr_accounts = models.CharField(max_length = 15,blank=True)
    #book_name = models.CharField(max_length=30,blank=True)
    #author = models.CharField(max_length=15,blank=True)
    #publisher = models.CharField(max_length=15,blank=True)
    #BoolChoices = [(True,'Yes'),(False,'No')]
    #sms = models.BooleanField(choices=BoolChoices,default=False,blank=True)
    #sms = models.BooleanField(default=False)
    #sms = models.CharField(max_length=10,blank=True)
    full_name = models.CharField(max_length=15,blank=True)
    username = models.CharField(max_length=15,blank=True)#view?