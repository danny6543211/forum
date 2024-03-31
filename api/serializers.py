from rest_framework import serializers
from . import models

class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ['id']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ['id', 'user', 'nickname']