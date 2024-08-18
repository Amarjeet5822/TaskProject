
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User,related_name='teams')

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='projects')
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='owned_project')
    start_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return self.name
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    assignee = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='tasks')
    status = models.CharField(max_length=20,choices=[('done','Done'),('in_progress','In Progress'),('todo','TO DO')],default='todo')
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"