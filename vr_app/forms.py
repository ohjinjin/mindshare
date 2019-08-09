"""from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SignUpForm(UserCreationForm):
    name=forms.CharField(max_length=20)
    email = forms.EmailField(max_length=254, help_text='Required Valid address')
    evidence = forms.ImageField()
    gender_choice=[('waman','woman'),('man','man')]
    sex= forms.ChoiceField(choices=gender_choice, widget=forms.RadioSelect)
    birth_date = forms.DateTimeField(help_text=' -을 포함하여 년도-월-일로 구분해주세요')
    phone_number = forms.CharField(max_length=11, help_text='전화번호는 - 을 포함하여 형식에 맞게 9-15자리로 써주세요')
    agreement = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, 'No'), (True, 'Yes')), widget=forms.RadioSelect )
    class Meta:
        model = User
        fields = ('first_name','last_name','username' , 'email', 'evidence', 'sex','birth_date','phone_number','password1','password2','agreement')
    def save(self,commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.sex = self.cleaned_data["sex"]
        user.birth_date = self.cleaned_data["birth_date"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.agreement = self.cleaned_data["agreement"]
        if commit:
            user.save()
        return user

"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile2
from ms_app.models import Library ####
from .models import Apply   ###



class SignUpForm2(UserCreationForm):
    test_record = forms.FileField()
    gender_choice=[('woman','여성'),('man','남성')]
    sex= forms.ChoiceField(choices=gender_choice, widget=forms.RadioSelect())
    birth_date = forms.DateTimeField(help_text='YYYY-MM-DD')
    phone_valid = RegexValidator(regex=r'^\d{3}-\d{3,4}-\d{4}$', message="000-0000-0000")
    phone_number = forms.CharField(validators=[phone_valid],max_length=13)
    agreement1 = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, '아니오'), (True, '예')), widget=forms.RadioSelect )
    agreement2 = forms.TypedChoiceField(coerce=lambda x: x =='True', choices=((False, '아니오'), (True, '예')), widget=forms.RadioSelect )
    """accept_choice=[('yes','yes'),('no','no')]
    agreement1= forms.ChoiceField(choices=accept_choice, widget=forms.RadioSelect)
    agreement2= forms.ChoiceField(choices=accept_choice, widget=forms.RadioSelect)"""
    class Meta:
        model = User 
        fields = ('first_name','last_name','username' , 'email', 'test_record','sex','birth_date','phone_number','password1','password2','agreement1', 'agreement2')
        
    # ohjinjin, 08/03/19 AM 01:52
    # 이 함수 두개는 파라미터 주면서 통일 가능한지 확인해보도록 하겠습니다
    def clean_agreement1(self):
        data = self.cleaned_data.get('agreement1')
        if data == self.fields['agreement1'].choices[0][0]:
            raise forms.ValidationError('동의1 : 필수동의입니다.')
        return data
    
    def clean_agreement2(self):
        data = self.cleaned_data.get('agreement2')
        if data == self.fields['agreement2'].choices[0][0]:
            raise forms.ValidationError('동의2 : 필수동의입니다.')
        return data



################## forms.py 수정 찬호 8_8 ######################       
class LibraryForm(forms.ModelForm):
    """title = forms.CharField(max_length=30)
    author = forms.CharField(max_length=30)
    publisher = forms.CharField(max_length=30)
    record = forms.FileField()
    pub_date = forms.CharField(max_length=30)
"""
    class Meta:
        model = Library
        #fields = ['title', 'author', 'publisher', 'record']
        fields = ['title', 'author', 'publisher', 'record', 'pub_date']
        
# ex) 1365 | ohjinjin | 니체의 말 | 니체 | 삼호미디어 | True | 실명 | 게시물작성자(ms의 username)
class ApplyForm(forms.ModelForm):
    #
    whichOrgan=[('1365','1365'),('VMS','VMS')]#얘를 모델에서 받을떄 charfield로 받아서 저장
    vms_or_1365= forms.ChoiceField(choices=whichOrgan, widget=forms.RadioSelect())#계정
    vr_accounts = forms.CharField(max_length=15)
    #book_name = forms.CharField(max_length=30)
    #author = forms.CharField(max_length=15)
    #publisher = forms.CharField(max_length=15)
    #
    # sms = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = Apply
        
        #primarykey==Library obj
        #1365 or VMS 라디오로
        #id 봉사계정
        #실명, username은 자동저장되야하니까 모델에 있어야함
        #책이름
        #저자
        #출판사
        #연락처로 sms수신하실지 여부 체크박스로
        #검색기능은 분리하기 ㅎㅎ
        #찬호님 이거 음 그 보여지는 폼들을 전부 적는 방향으로할게용 !?
        #잘 이해가 .. 템플릿에서 전부 적는다는 말씀인가요? {{form.sms }}이런식 ? 네네!!!
        #fields = ['primarykey', 'm_1365_id', 'privacy']
        fields = ['vms_or_1365','vr_accounts']
        #exclude = ['is_deleted'] 
        #widgets = {
        #    'is_anything_required' : CheckboxInput(),
        #}
###############################################################
class Profile2Form(forms.ModelForm):
    class Meta:
        model = Profile2
        fields = ['mileage']