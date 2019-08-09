from django.urls import path
from . import views
from ms_app import views as ms_views #test(son)
#from django.views.generic import TemplateView

urlpatterns = [
    path('vr_signup/', views.CreateUserView2.as_view(), name ='vr_signup'),
    path('vr_index/', views.vr_index, name = 'vr_index'), 
    #path('vr_signup/', views.vr_signup, name ='vr_signup'),
    path('vr_login/', views.vr_login, name ='vr_login'),
    path('logout/',views.logout, name='logout'),
    path('apply/', views.apply, name = 'apply'),
    path('vr_help/', views.vr_help, name = 'vr_help'),
    path('about/', views.about, name = 'about'),
    path('qna/',views.qna,name='qna'),
    # path('create/',views.create, name='create'),
    path('qscreate/',views.qscreate,name='qscreate'),
    path('question_info/<int:question_id>/',views.question_info,name='question_info'),
    path('question_info/<int:question_id>/delete/',views.delete,name='delete'),
    path('<int:question_id>/modify/',views.modify,name='modify'),
    path('<int:question_id>/qnamodify/',views.qnamodify,name='qnamodify'),
    path('vr_mypage/',views.vr_mypage,name='vr_mypage'),
    path('vr_mypage/transmile',views.transmile,name='transmile'),
    path('wish_book_list/',ms_views.lists, name='wish_book_list'), #test(son)
    path('apply_choice/',views.apply_choice, name='apply_choice'),
    path('<int:question_id>/comment_new', views.comment_write, name="comment_write"),
    
]