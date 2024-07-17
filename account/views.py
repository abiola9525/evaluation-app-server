from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework import status, serializers
import random
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from account.models import User
from . serializers import MyTokenObtainPairSerializer, UserSerializer, ResetPasswordSerializer, UpdateUserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.permissions import IsAuthenticated
import uuid

@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def register_user(request):
    data = request.data

    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        user.save()

        return Response({
                'message': 'User Account Created Successfully',
                'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
@swagger_auto_schema(method='PUT', request_body=UpdateUserSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def user_details(request):
    if request.method == "GET":
        
        user_serializer = UserSerializer(request.user)
        data = user_serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        user_serializer = UpdateUserSerializer(request.user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)
        
@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    try:
        user.delete()
        return JsonResponse({'message': 'User account deleted successfully.'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@swagger_auto_schema(method='POST', request_body=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    
    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='POST', request_body=ForgotPasswordSerializer)
@api_view(['POST'])
def send_reset_password_email(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email=email, is_active=True)
        
        # Generate a four-digit confirmation code
        confirmation_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        
        # Save the code in the user's profile (you may need to create a profile model)
        user.confirmation_code = confirmation_code
        user.save()
        
        # Send confirmation email
        confirmation_message = f'Your confirmation code for password reset is: {confirmation_code}'
        send_mail(
            'Reset Your Password',
            confirmation_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'A password reset confirmation code has been sent to your email.'})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=ResetPasswordSerializer)
@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    confirmation_code = serializer.validated_data['confirmation_code']
    new_password = serializer.validated_data['new_password']

    try:
        # Find the user by confirmation code
        user = User.objects.get(confirmation_code=confirmation_code, is_active=True)
        
        # Reset user password
        user.set_password(new_password)
        user.save()
        
        # Clear the confirmation code
        user.confirmation_code = ''
        user.save()
        
        return JsonResponse({'message': 'Password reset successfully.'})
    except User.DoesNotExist:
        return JsonResponse({'message': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)