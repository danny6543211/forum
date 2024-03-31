from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserProfile
from .permissions import UserProfileDetailPermission
from .serializers import UserProfileSimpleSerializer, UserProfileDetailSerializer


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
        user_profile = UserProfile.objects.get(user=user)
        serializer = UserProfileDetailSerializer(user_profile)
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
    serializer = UserProfileSimpleSerializer(data={'user': user.id, 'nickname': nickname})
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'User created successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    permission_classes = [UserProfileDetailPermission]

