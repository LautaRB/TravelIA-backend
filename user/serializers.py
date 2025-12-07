from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from travelia.utils.messeges import MessagesES

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    remove_profile_picture = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role', 'profile_picture', 'remove_profile_picture', 'currency', 'distance_unit']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def get_profile_picture(self, obj):
        return obj.profile_picture_url
    
    def validate_username(self, value):
        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_USERNAME_TYPE)
        return value
    
    def create(self, validated_data):
        validated_data.pop('remove_profile_picture', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        instance.currency = validated_data.get('currency', instance.currency)
        instance.distance_unit = validated_data.get('distance_unit', instance.distance_unit)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            
        if validated_data.get("remove_profile_picture"):
            instance.profile_picture = "profile_pictures/default.png"
        elif "profile_picture" in validated_data:
            instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        
        instance.save()
        return instance
    
    def validate_currency(self, value):
        valid_currencies = dict(User.CURRENCY_CHOICES).keys()
        if value not in valid_currencies:
            raise serializers.ValidationError(MessagesES.ERROR_CURRENCY_TYPE)
        return value

    def validate_distance_unit(self, value):
        valid_units = dict(User.UNIT_CHOICES).keys()
        if value not in valid_units:
            raise serializers.ValidationError(MessagesES.ERROR_DISTANCE_UNIT_TYPE)
        return value
