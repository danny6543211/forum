from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()


urlpatterns = [
    path('user/login/', views.user_login),
    path('user/register/', views.user_register),
    
    path('profile/', views.ProfileList.as_view()),
    path('profile/<int:pk>/', views.ProfileUpdate.as_view()),
    

    path('', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
