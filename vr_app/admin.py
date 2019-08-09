from django.contrib import admin
from .models import HelpData
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile2
from django.contrib.admin import AdminSite
from .models import Apply
class VRAdminSite(AdminSite):
    site_header = "MindShare VR Admin"
    site_title = "MindShare VR Admin Portal"
    index_title = "Welcome to MindShare VR Portal"

vr_admin_site = VRAdminSite(name="vr_admin")

# Register your models here.
#admin.site.register(HelpData)
vr_admin_site.register(HelpData)

class ProfileInline2(admin.StackedInline):
    model = Profile2
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline2,)

#admin.site.unregister(User)
#admin.site.register(User,UserAdmin)
vr_admin_site.register(User,UserAdmin)
vr_admin_site.register(Apply) #### 8_8 추가 찬호 
