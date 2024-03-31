from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import User



class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
    
class ArticlePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # article'is user named 'author'
        return obj.author == request.user