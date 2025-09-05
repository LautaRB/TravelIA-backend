from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from travelia.utils.messeges import MessagesES
from travelia.settings import DEFAULT_PROFILE_PICTURE

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    remove_profile_picture = serializers.BooleanField(write_only=True, required=False, default=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role', 'profile_picture', 'remove_profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def get_profile_picture(self, obj):
        return obj.profile_picture or DEFAULT_PROFILE_PICTURE
    
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

        if validated_data.get("remove_profile_picture"):
            instance.profile_picture = "profile_pictures/default.png"
        elif "profile_picture" in validated_data:
            instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        
        instance.save()
        return instance
