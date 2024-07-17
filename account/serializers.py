from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from account.backends import CustomAuthenticationBackend

from . models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['user_code'] = user.user_code
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_staff

        return token
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Use your custom authentication backend to authenticate the user
        user = CustomAuthenticationBackend().authenticate(request=None, username=username, password=password)

        if user is None:
            # Check if user exists to differentiate between incorrect password and non-existent user
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"detail": "User does not exist."})
            else:
                raise serializers.ValidationError({"detail": "Incorrect password."})

        data = super().validate(attrs)
        # Add additional custom claims if needed
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "gender", "is_user", "password"]
        read_only_fields = ["is_user"]
        extra_kwargs = {
                    'password': {'write_only': True}
                }
        
    def create(self, validated_data):
        user = User.objects.create(
                    username= validated_data['username'],
                    email=validated_data['email'],
                    first_name = validated_data['first_name'],
                    last_name = validated_data['last_name'],
                    gender = validated_data['gender'],
                    is_user=True,  
                )
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # set email to read only on update
    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['email'].read_only = True
        return fields
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id', 'email', 'username', "first_name", "last_name", "gender", 'is_user', 'is_admin']
        read_only_fields = ['email', 'is_user', 'is_admin']
        
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)