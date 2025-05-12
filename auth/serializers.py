from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from backend.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password', 'full_name', 'zip_code']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims if needed
        token = self.get_token(self.user)
        
        # Add user data to response
        data.update({
            'user': {
                'id': self.user.id,
                'email': self.user.email,
                'full_name': self.user.full_name,
                'phone_number': self.user.phone_number,
                'zip_code': self.user.zip_code
            }
        })
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        data['user'] = user
        return data
