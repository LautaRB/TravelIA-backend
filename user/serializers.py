from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from travelia.utils.messeges import MessagesES

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    remove_profile_picture = serializers.BooleanField(required=False, default=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role', 'profile_picture', 'remove_profile_picture', 'currency', 'distance_unit']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'profile_picture': {'required': False}
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if hasattr(instance, 'profile_picture_url'):
            rep['profile_picture'] = instance.profile_picture_url 
        return rep

    def validate_username(self, value):
        if " " in value:
            raise serializers.ValidationError(MessagesES.ERROR_USERNAME_SPACES)

        if value.isdigit():
            raise serializers.ValidationError(MessagesES.ERROR_USERNAME_TYPE)
        
        if User.objects.filter(username=value).exists(): 
            raise serializers.ValidationError(MessagesES.ERROR_USER_ALREADY_EXISTS)
            
        return value

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
            instance.profile_picture = None
        elif "profile_picture" in validated_data:
            instance.profile_picture = validated_data.get("profile_picture", instance.profile_picture)
        
        instance.save()
        return instance