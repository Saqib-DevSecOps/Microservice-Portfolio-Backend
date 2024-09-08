from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Remove the username field
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password1']
        )
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove the username field
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], username=kwargs.get('email'), password=kwargs.get('password'))
