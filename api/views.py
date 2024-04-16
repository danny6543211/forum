from django.contrib.auth import authenticate
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, Comment, User, UserProfile
from .serializers import UserProfileSerializer, ArticleSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
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
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        # 判断是否篡改 id
        if request.user.id != int(request.data['user']):
            return Response({'msg': 'User id incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny]) 
    def comments(self, request):
        queryset = Comment.objects.all().filter(article=request.data['article'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        # 判断是否篡改 id
        if request.user.id != int(request.data['user']):
            return Response({'msg': 'User id incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    

