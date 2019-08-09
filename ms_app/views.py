from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .forms import SignUpForm1
#from .models import Profile
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm # 장고의 기본적인 회원가입 폼. id, password만 확인한다는 한계점.
from django.urls import reverse_lazy
from django.contrib import auth
from .models import Profile1
from .models import Wish_Book
from .models import Library
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
"""def ms_signup(request):
    if request.method == 'POST':
        if request.POST['ms_password1'] == request.POST['ms_password2']:
            ms_user = User.objects.create_user(request.POST['ms_username'],email=request.POST['ms_email'],password=request.POST['ms_password1'])
            auth.login(request, ms_user)
            return redirect('index.html') # ms 페이지 이동
    #return render(request, 'accounts/ms_signup.html')
    return render(request, 'ms_signup.html',{'error':'회원가입 실패'})    # ohjinjin 문장 수정"""

class CreateUserView1(CreateView):  # 제네릭의 CreateView는 폼하고 연결돼서, 혹은 모델하고 연결돼서 새로운 데이터를 넣을 때 사용.
   
    template_name = 'ms_signup.html'     # 회원가입 할 때 띄울 폼 템플릿
    form_class = SignUpForm1
    success_url = reverse_lazy('ms_index') # 성공하면 어디로 갈지, url name
    # 여기서 reverse가 아닌 reverse_lazy를 사용하는 이유: 제네릭뷰 같은경우 타이밍 문제 때문에 reverse_lazy를 사용해야함

    def form_valid(self,form):
        c = {'form':form,}
        user = form.save(commit=False)  #여기서 default User model과 profile이 엮여서 db에 저장되는듯합니다. 
        #email = form.cleaned_data["email"]
        #password1 = form.cleaned_data['password1']
        #password2 = form.cleaned_data['password2']
        evidence = form.cleaned_data["evidence"]
        sex = form.cleaned_data["sex"]
        birth_date = form.cleaned_data["birth_date"]
        phone_number = form.cleaned_data["phone_number"]
        agreement1 = form.cleaned_data["agreement1"]
        agreement2 = form.cleaned_data["agreement2"]
        agreement3 = form.cleaned_data["agreement3"]
        
        """if password1 != password2:
            messages.error(self.request, "Passwords do not Match", extra_tags = 'alert alert-danger')
            return render(self.request, self.template_name, c)"""
        #user.set_password(password1)
        user.save()

        Profile1.objects.create(user=user, phone_number=phone_number, birth_date = birth_date, evidence=evidence,sex=sex,agreement1=agreement1,agreement2=agreement2,agreement3=agreement3)

        return super(CreateUserView1, self).form_valid(form)


class RegisteredView(TemplateView): # 회원가입이 완료된 경우
    template_name = 'ms_index.html'

@login_required
def lists(request):
    #wbooks=Wish_Book.objects.all()
    tmpWbooks = Wish_Book.objects.all()
    paginator = Paginator(tmpWbooks, 6)
    page = request.GET.get('page')
    wbook_list = paginator.get_page(page)

    return render(request,'list.html',{'wbooks': tmpWbooks.order_by('id').reverse().all(),'wbook_list':wbook_list})

def ms_login(request):
    # 해당 쿠키에 값이 없을 경우 None을 return 한다.
    if request.COOKIES.get('ID') is not None:
        username = request.COOKIES.get('ID')
        password = request.COOKIES.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("ms_index")  
        else:
            return render(request, "ms_login.html")

    elif request.method == "POST":
        username = request.POST["inputid"]
        password = request.POST["inputpassword"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)
        obj = None
        for eachProf in Profile1.objects.all():
            if eachProf.user.username == username:
                obj = eachProf
                break
        if user is not None and obj is not None:
            auth.login(request, user)
            if request.POST.get("keep_login") == "TRUE":
                response = render(request, 'ms_index.html')
                response.set_cookie('ID',username)
                response.set_cookie('password',password)
                return response
            return redirect('ms_index')
        else:
            if user is None:
                msg = "id/pw incorrect"
            else:
                msg = "Inaccessible"
            return render(request, 'ms_login.html', {'error':msg})
    else:
        return render(request, 'ms_login.html')
    return render(request, 'ms_login.html')


# def ms_login(request):
#     if request.method == "POST":
#         username = request.POST['ID']
#         password = request.POST['password']
#         user = auth.authenticate(request, username = username, password = password)
#         obj = None
#         msg = ""
#         for eachProf in Profile1.objects.all():
#             if eachProf.user.username == username:
#                 obj = eachProf
#                 break
        
#         if user is not None and obj is not None:
#             auth.login(request,user)
#             return render(request, 'ms_index.html', {'customedUser' : obj})
#         else:
#             if user is None:
#                 msg = "id/pw incorrect"
#             else:
#                 msg = "Inaccessible"
#             return render(request, 'ms_login.html',{'error' : msg})
#     # return render(request, 'accounts/vr_login.html')
#     return render(request, 'ms_login.html') # ohjinjin 臾몄옣 異붽��

def ms_logout(request):
    response = render(request,'index.html')
    response.delete_cookie('ID')
    response.delete_cookie('password')
    auth.logout(request)
    return redirect('index')

def ms_index(request):
    return render(request, 'ms_index.html')

def ms_mypage(request):
    return render(request, 'ms_mypage.html')

@login_required
def ms_library(request):
    #db table 이미 만들어져있어야되고 걔네를 불러와줘야함 다운로드가능하게해줘야함_ohjinjin 080619 PM15:08
    bookList=Library.objects
    paginator = Paginator(bookList.all(), 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)

    return render(request,'ms_library.html',{'bookList': bookList, 'books':books})
    
@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def wish_books(request):
    return render(request, 'wish_books.html')

@login_required
def create(request):
    wbook = Wish_Book()
    wbook.title = request.GET['book_name']
    wbook.author = request.GET['book_author']
    wbook.publisher = request.GET['book_publish']
    wbook.pub_date = request.GET['book_year']
    wbook.save()
    return redirect('/ms/ms_index/')

@login_required
def mybooks(request):
    return render(request, 'mybooks.html')

@login_required
def listening_page(request,book_id):
    booklist = get_object_or_404(Library,pk=book_id)
    return render(request, 'listening_page.html',{'booklist':booklist})
    
