from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions, viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserProfile, Article
from .permissions import IsOwnerOrReadOnly, ArticlePermission
from .serializers import UserProfileSerializer, ArticleSerializer


class UserViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['POST'])
    def login(self, request):
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
            serializer = UserProfileSerializer(user_profile)
            return Response({'msg': 'Login successful.', 'token': token.key, "user_profile": serializer.data}, 
                            status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])    
    def register(self, request):
        username = request.data['username']
        password = request.data['password']
        nickname = request.data['nickname']

        if not username or not password:
            return Response({'msg': 'Both username and password are required.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'msg': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)       
        serializer = UserProfileSerializer(data={'user': user.id, 'nickname': nickname})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermission]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # reload update......