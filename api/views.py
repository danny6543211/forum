from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .models import Profile
from .serializers import ProfileListSerializer, ProfileUpdateSerializer
from .permissions import ProfilePermission

@api_view(['post'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    if not username or not password:
        return Response({'msg': 'Both username and password are required.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user:
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile)
        return Response({'msg': 'Login successful.', 'token': token.key, "user_profile": serializer.data}, 
                        status=status.HTTP_200_OK)
    else:
            return Response({'msg': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['post'])
def user_register(request):
    username = request.data['username']
    password = request.data['password']
    nickname = request.data['nickname']

    if not username or not password:
        return Response({'msg': 'Both username and password are required.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'msg': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)       
    serializer = ProfileSerializer(data={'user': user.id, 'nickname': nickname})
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User created successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = [ProfilePermission]

class ProfileUpdate(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [ProfilePermission]
    
    def partial_update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
