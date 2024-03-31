from rest_framework import serializers
from . import models


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['user', 'nickname'] #......

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        exclude = ['user']


# class ArticleSimpleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Article
#         fields = '__all__'

# class ArticleDetialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Article
#         fields = '__all__'