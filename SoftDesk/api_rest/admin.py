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


class ContributorsAdmin(admin.ModelAdmin):
    list_filter = [("project", admin.RelatedOnlyFieldListFilter)]
    list_display = ["user", "project"]
    ordering = ["project"]


class IssuesAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    list_display = ["title", "project", "status"]
    ordering = ["project"]


class ProjectsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Users, UserAdmin)
admin.site.register(Contributors, ContributorsAdmin)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Issues, IssuesAdmin)
admin.site.register(Comments)
admin.site.unregister(Group)
