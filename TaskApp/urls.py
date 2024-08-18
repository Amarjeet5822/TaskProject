from django.urls import path,re_path
from .views import UserLogin,UserSignup,ProjectCreate,ProjectDetail,TeamDetail,TeamListCreate,TaskCreate,TaskDetail,CommentDetail,CommentCreate,UserLogout
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Task Master Project",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('signup/',UserSignup.as_view(),name='user_signup'),
    path('login/',UserLogin.as_view(),name='user_login'),
    path('logout/',UserLogout.as_view(),name='user_logout'),

    path('teams/',TeamListCreate.as_view(),name="team_create"),
    path('teams/<int:pk>/',TeamDetail.as_view(),name="team_update_delete"),

    path('projects/',ProjectCreate.as_view(),name='project_create'),
    path('projects/<int:pk>/',ProjectDetail.as_view(),name='project_update_delete'),

    path('tasks/',TaskCreate.as_view(),name='task_create'),
    path('tasks/<int:pk>/',TaskDetail.as_view(),name='task_update_delete'),

    path('comments/',CommentCreate.as_view(),name='comment_create'),
    path('comments/<int:pk>/',CommentDetail.as_view(),name='comment_update_delete'),

#  Swagger 
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

