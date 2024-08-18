from django.shortcuts import render,get_object_or_404
from .serializers import UserSerializer,ProjectSerializer,TeamSerializer,TaskSerializer,CommentSerializer,RegisterSerializer
from .models import Project,Team,Task,Comment
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.views.decorators.csrf import csrf_exempt
import jwt,datetime
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
class CustomPagination(PageNumberPagination):
    page_size = 1 # Customize the page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSignup(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request,*args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # email = request.data.get('email')
        # if User.objects.filter(email=email):
        #     return Response({'message':"Email Already taken!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if User.objects.filter(username=username).exists():
            return Response({'message':"Username already taken"},status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'Signup Successfull'},status=status.HTTP_200_OK)
        return Response({'message':'something went wrong! Signup again'},status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print('line 45 ',user.id)
        if user is not None:
            # payload = {
            #     'id':user.id,
            #     'iat':datetime.datetime.now(datetime.UTC),
            #     'exp':datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=120)
            # }
            # token = jwt.encode(payload,'cap01_046',algorithm='HS256')
            # print(token)
            return Response({'message':'login Successfull'},status=status.HTTP_201_CREATED)
        return Response({'message':'Credential invalid'},status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def post(self,request):
        logout(request)        
        return Response({'message':'logout Successfull'},status = status.HTTP_200_OK)
        # response.data = {'message':'logout Successfull'}
        # response.status = status.HTTP_200_OK
        # response.delete_cookie('jwt')
        # return response
    
class TeamListCreate(APIView):
    
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    
    def get(self,request,*args,**kwargs):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username)
            teams = Team.objects.all()
            print("teams of Main user = ",teams)
            serializer=TeamSerializer(teams,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({'detail':"Post not found"},status=status.HTTP_204_NO_CONTENT)
    
    def post(self,request):
        user = request.data.get('USER')
        # print(user)
        user = User.objects.filter(id=user).first()
        # print(user)
        if user:
            print(request.data)
            serializer= TeamSerializer(data=request.data)
            if serializer.is_valid():
                # print(serializer.data)
                serializer.save()
                return Response({'message':'Team Created'},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail':'Unauthorized User! Register yourself, Developer need to redirect this user to register or signup page'})
class TeamDetail(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def getObject(self,pk):
        try:
            team = Team.objects.get(id=pk)
            return team
        except Team.DoesNotExist:
            return Response({'message':'Team not Exist'})
    
    def get(self,request,pk):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username)
            team = get_object_or_404(Team,pk=pk)
            if team.members == user:
                serializer = TeamSerializer(team)
                return Response(serializer.data)
            
    
    def put(self,request,pk):
        team = get_object_or_404(Team,pk=pk)
        serializer = TeamSerializer(team,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        team = get_object_or_404(pk=pk)
        team.delete()
        return Response({'message':'Team Deleted'},status=status.HTTP_204_NO_CONTENT)
    
class ProjectCreate(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Project Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ProjectDetail(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        serializer = ProjectSerializer(project,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Project Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskCreate(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self,request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'task Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class TaskDetail(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        serializer = TaskSerializer(tasks)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        serializer =TaskSerializer(tasks,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'task Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentCreate(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self,request):
        comments= Comment.objects.all()
        serializer = CommentSerializer(comments,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'project Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class CommentDetail(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self,request,pk):
        comments = get_object_or_404(Comment,pk=pk)
        serializer = CommentSerializer(comments)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        comments= get_object_or_404(Comment,pk=pk)
        serializer =CommentSerializer(comments,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Comment Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        comments = get_object_or_404(Comment,pk=pk)
        comments.delete()
        return Response({'detail':"Comment is Deleted! "},status=status.HTTP_204_NO_CONTENT)
    
# Swagger 

