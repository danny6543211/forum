from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User

# Create your views here.
class UserAPI(viewsets.GenericViewSet):
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'msg': 'Both username and password are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        User.objects.create_user(username=username, password=password)
        return Response({'msg': 'User created successfully.'}, status=status.HTTP_201_CREATED)

            