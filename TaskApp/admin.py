from django.contrib import admin
from .models import Task,Team,Project,Comment

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','project','assignee','status','due_date','created_at','updated_at']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','team','owner','start_date','due_date']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','task','author','content','created_at']

admin.site.register(Task,TaskAdmin)
admin.site.register(Team,TeamAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Comment,CommentAdmin)
