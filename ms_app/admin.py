from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile1
from django.contrib.admin import AdminSite
from .models import Wish_Book
from .models import Library
class MSAdminSite(AdminSite):
    site_header = "MindShare MS Admin"
    site_title = "MindShare MS Admin Portal"
    index_title = "Welcome to MindShare MS Portal"

ms_admin_site = MSAdminSite(name="ms_admin")

class ProfileInline1(admin.StackedInline):
    model = Profile1
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline1,)

ms_admin_site.register(User,UserAdmin)
#admin.site.unregister(User)
#admin.site.register(User,UserAdmin)
# from .forms import SignUpForm
# admin.site.register(SignUpForm)

ms_admin_site.register(Wish_Book)
ms_admin_site.register(Library)