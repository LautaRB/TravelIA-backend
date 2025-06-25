from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from travelia.utils.messeges import MessagesES

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role']
        extra_kwargs = {
                        'password': {'write_only': True},
                        'email': {'required': True}
                        }
    
    def validate_username(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_USERNAME_TYPE)
        return value
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance