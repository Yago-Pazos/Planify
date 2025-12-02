from django.contrib import admin

from .models import User, AuthToken, Project, Task

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','created_at')
    search_fields = ('name','email')

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user','key','created_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at')
    search_fields = ('name',)
    filter_horizontal = ('members',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','project','state','assigned_to','created_at')
    list_filter = ('state','project')




