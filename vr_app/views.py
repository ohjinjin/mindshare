from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .forms import SignUpForm2
#from .forms import SignUpForm
from django.contrib import auth
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import HelpData
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Profile2
import ms_app.models
from django.core.paginator import Paginator
# from django.contrib import messages
# from .models import Comment
from .forms import ApplyForm
from .forms import LibraryForm
from .models import Apply
from ms_app.models import Library
from django.utils import timezone
from django.core import serializers #for js
from .forms import Profile2Form
from ms_app.models import Wish_Book
def index(request): # ohjinjin 함수 추가
    return render(request,'index.html')

def vr_login(request):
    # 해당 쿠키에 값이 없을 경우 None을 return 한다.
    if request.COOKIES.get('inputid') is not None:
        username = request.COOKIES.get('inputid')
        password = request.COOKIES.get('inputpassword')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("vr_index")  
        else:
            return render(request, "vr_login.html")
    elif request.method == "POST":
        username = request.POST["inputid"]
        password = request.POST["inputpassword"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)
        obj = None
        # msg = ""
        for eachProf in Profile2.objects.all():
            if eachProf.user.username == username:
                obj = eachProf
                break
        if user is not None and obj is not None :
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE":
                response = render(request, 'vr_index.html')
                response.set_cookie('inputid',username)
                response.set_cookie('inputpassword',password)
                return response
            return redirect('vr_index')
        else:
            if user is None:
                msg = "id/pw incorrect"
            else:
                msg = "Inaccessible"
            return render(request, 'vr_login.html', {'error':msg})
    else:
        return render(request, 'vr_login.html')
    return render(request, 'vr_login.html')

# def vr_login(request):
#     # ohjinjin 함수 전반적으로 수정
#     if request.method == "POST":
#         username = request.POST['ID']
#         password = request.POST['vr_password']
#         user = auth.authenticate(request, username = username, password = password)
#         obj = None
#         msg = ""
#         for eachProf in Profile2.objects.all():
#             if eachProf.user.username == username:
#                 obj = eachProf
#                 break

#         if user is not None and obj is not None:
#             auth.login(request,user)
#             return render(request, 'vr_index.html', {"customedUser":obj})
#         else:
#             if user is None:
#                 msg = "id/pw incorrect"
#             else:
#                 msg = "Inaccessible"
#             return render(request, 'vr_login.html',{'error' : msg})
#     #return render(request, 'accounts/vr_login.html')
#     return render(request, 'vr_login.html') # ohjinjin 문장 추가

"""def vr_signup(request):
    return render(request,'vr_signup.html')"""

    
def logout(request):
    response = render(request,'vr_index.html')
    response.delete_cookie('inputid')
    response.delete_cookie('inputpassword')
    auth.logout(request)
    return redirect('vr_index')

############################## views.py apply 수정 8_8 찬호 ############
def apply(request):
    username = request.user.username
    last_name = request.user.last_name
    first_name = request.user.first_name
    obj3=None
    for eachProf in Profile2.objects.all():
        if eachProf.user.username == username:
            obj3 = eachProf
            break
    if request.method=='POST':
        form1 = LibraryForm(request.POST, request.FILES)
        form2 = ApplyForm(request.POST)
        form3 = Profile2Form(request.POST)
        frommile=obj3.mileage
        if form1.is_valid() and form2.is_valid() and form3.is_valid(): # 수정 
            obj = Library(title=form1.data['title'], author=form1.data['author'], publisher=form1.data['publisher'], record=request.FILES['record'], pub_date=form1.data['pub_date'])
            obj.save()
            ##obj2 = Apply(primarykey=obj , writer=username, date = timezone.datetime.now(), vms_1365_id=form2.data['vms_1365_id'], writer_name=form2.data['writer_name'] )
            obj2 = Apply(primarykey=obj ,vr_accounts=form2.data['vr_accounts'], username=username, vms_or_1365=form2.data['vms_or_1365'], full_name = last_name+first_name)
            ##obj = form.save(commit=False)
            ##obj.writer = username
            ##obj.pub_date=timezone.now()
            obj2.save()
            mileage_= int(form3.data['mileage']) + int(frommile)
            obj3.mileage = mileage_
            obj3.save()
            return redirect('vr_index')
        else:
            library = Library.objects.all()
            for eachBook in library:
                if request.POST.get(eachBook.title,'') == "on":
                    return render(request, 'apply.html', {'Abook':eachBook})
                #pass
       #     choice = request.POST['{{wbook_title}}']
            # wbook = Wish_Book.objects.all()
            # for book in wbook.title:
            #     if wbook.title == choice:

            ##test(son)
            pass
        
        return redirect('vr_index')
    else:
        form1 = ApplyForm()
        form2 = LibraryForm()
        form3 = Profile2Form()

        wishbooks = Wish_Book.objects.all()
        
        list_of_input_ids = request.GET.get("boook")
        if list_of_input_ids!=None:
            return render(request,'apply.html', {'Abook':list_of_input_ids,'wishbooks':wishbooks,'form1':form1, 'form2':form2, 'form3':form3})
        
        return render(request, 'apply.html', {'form1':form1, 'form2':form2, 'form3':form3})
#####################################################################

def vr_help(request): 
    question =HelpData.objects
    question_list = HelpData.objects.all()
    paginator = Paginator(question_list,10)
    page = request.GET.get('page')
    questions = paginator.get_page(page)
    return render(request, 'vr_help.html',{'question':question,'questions':questions})

def about(request):
    return render(request, 'about.html')

def vr_index(request):  # 추가 chanho - 19_8_2_13:50
    return render(request, 'vr_index.html')

def qna(request):
    return render(request,'qna.html')

def qscreate(request):
    question = HelpData()
    question.question_title = request.GET['question_title']
    question.question_content = request.GET['question_content']
    question.pub_date =timezone.datetime.now()
    question.save()
    return redirect('vr_help')

"""class CreateUserView(CreateView):  # 제네릭의 CreateView는 폼하고 연결돼서, 혹은 모델하고 연결돼서 새로운 데이터를 넣을 때 사용.
    template_name = 'vr_signup.html'     # 회원가입 할 때 띄울 폼 템플릿
    form_class = SignUpForm
    success_url = reverse_lazy('vr_index') # 성공하면 어디로 갈지, url name
    # 여기서 reverse가 아닌 reverse_lazy를 사용하는 이유: 제네릭뷰 같은경우 타이밍 문제 때문에 reverse_lazy를 사용해야함

    def form_valid(self,form):
        c = {'form':form,}
        user = form.save(commit=False)  #여기서 default User model과 profile이 엮여서 db에 저장되는듯합니다.
        evidence = form.cleaned_data["evidence"]
        sex = form.cleaned_data["sex"]
        birth_date = form.cleaned_data["birth_date"]
        phone_number = form.cleaned_data["phone_number"]
        agreement = form.cleaned_data["agreement"]
        
        user.save()

        Profile2.objects.create(user=user, phone_number=phone_number, birth_date = birth_date, evidence=evidence,sex=sex,agreement=agreement)

        return super(CreateUserView, self).form_valid(form)
"""
def question_info(request,question_id):
    question = get_object_or_404(HelpData,id=question_id)
    return render(request,'question_info.html',{'question':question})

def delete(request,question_id):
    question = HelpData.objects.get(id=question_id)
    question.delete()
    return redirect('vr_help')

def vr_mypage(request):
    user=request.user
    username=request.user.username
    frommile=request.user.profile2.mileage
    realmile2=request.user.profile2.realmile
    canmile = int(frommile)//60
    return render(request, 'vr_mypage.html',{'frommile':frommile, 'realmile2' : realmile2, 'canmile' : canmile})

def transmile(request):
    username = request.user.username
    obj=None
    for eachProf in Profile2.objects.all():
        if eachProf.user.username == username:
            obj = eachProf
            break
    
    if request.method=='POST':
        frommile = obj.mileage
        tomile= obj.realmile
        wanttomile2 = request.POST.get('wanttomile')
        if(wanttomile2=="NULL"):
            return redirect('vr_mypage')
        elif(int(int(wanttomile2)*60)>int(frommile)):
            pass
        else:
            frommile = int(int(frommile) - int(wanttomile2)*60)
            tomile = int(tomile) + int(wanttomile2)
        obj.mileage = frommile
        obj.realmile = tomile
        obj.save()
        return redirect('vr_mypage')


def modify(request,question_id):
    question = get_object_or_404(HelpData,pk=question_id)
    return render(request,'modify.html',{'question':question})

def qnamodify(request,question_id):
    question = get_object_or_404(HelpData,pk=question_id)
    question.question_title = request.POST['question_title']
    question.question_content = request.POST['question_content']
    question.save()
    return redirect('vr_help')

def apply_choice(request):
    json_serializer = serializers.get_serializer("json")()
    books = json_serializer.serialize(Library.objects.all(), ensure_ascii=False)
    return render(request,'apply_choice.html',{'books':books})



def comment_write(request,question_id):
    if request.method=='POST':
        question = get_object_or_404(HelpData,pk=question_id)
        content = request.POST.get('content')
        if not content:
            messages.info(request,"You don't write")
            return redirect('/vr/question_info/'+str(question_id))
        Comment.objects.create(question=questioin,comment_contents=content)
        return redirect('/vr/question_info/'+str(question_id))
##
class RegisteredView(TemplateView): # �쉶�썝媛��엯�씠 �셿猷뚮맂 寃쎌슦
    template_name = 'vr_index.html'



class CreateUserView2(CreateView):  # 제네릭의 CreateView는 폼하고 연결돼서, 혹은 모델하고 연결돼서 새로운 데이터를 넣을 때 사용.
    template_name = 'vr_signup.html'     # 회원가입 할 때 띄울 폼 템플릿
    form_class = SignUpForm2
    success_url = reverse_lazy('vr_index') # 성공하면 어디로 갈지, url name
    # 여기서 reverse가 아닌 reverse_lazy를 사용하는 이유: 제네릭뷰 같은경우 타이밍 문제 때문에 reverse_lazy를 사용해야함

    def form_valid(self,form):
        c = {'form':form,}
        user = form.save(commit=False)  #여기서 default User model과 profile이 엮여서 db에 저장되는듯합니다.
        test_record = form.cleaned_data["test_record"]
        sex = form.cleaned_data["sex"]
        birth_date = form.cleaned_data["birth_date"]
        phone_number = form.cleaned_data["phone_number"]
        agreement1 = form.cleaned_data["agreement1"]
        agreement2 = form.cleaned_data["agreement2"]
        
        user.save()

        Profile2.objects.create(user=user, phone_number=phone_number, birth_date = birth_date, test_record=test_record,sex=sex,agreement1=agreement1, agreement2=agreement2)

        return super(CreateUserView2, self).form_valid(form)

