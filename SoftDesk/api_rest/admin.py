from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Register your models here.
from api_rest.models import (
    Contributors,
    Projects,
    Issues,
    Comments,
    Users
)


admin.site.register(Users, UserAdmin)
admin.site.register(Contributors)
admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)
admin.site.unregister(Group)
