from rest_framework import serializers
from .models import Task,Team,Project,Comment
from django.contrib.auth.models import User

# User Serializers
from rest_framework import serializers
from .models import Team
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members','USER']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(**validated_data)
        team.members.set(members)
        return team


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            # email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
     )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        model = Project
        fields = ['name', 'description', 'team', 'owner', 'start_date', 'due_date']

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    # assignee_detail = UserSerializer(source='assignee', read_only=True)
    # project_detail = ProjectSerializer(source='project', read_only=True)

    class Meta:
        model = Task
        fields = ["title",'description','project','assignee','status','due_date']

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    task= serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['task','author','content']

    def create(self, validated_data):
        comment= Comment.objects.create(**validated_data)
        return comment