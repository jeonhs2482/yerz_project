from .models        import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user   = User.objects.all()
        model  = User
        fields = '__all__'

class UserBodySerializer(serializers.Serializer):
    email    = serializers.CharField(help_text="아이디")
    password = serializers.CharField(help_text="비밀번호")
    