from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_verification_link
from .serializers import SignupSerializer, LoginSerializer
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from rest_framework.permissions import IsAuthenticated


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_link = generate_verification_link(user, request)
            
            # Render the HTML email template
            html_message = render_to_string('welcome_verification_email.html', {
                'user': user,
                'verification_link': verification_link
            })
            
            # Create plain text version of the email
            plain_message = strip_tags(html_message)
            
            # Send the email
            email = EmailMessage(
                subject="Welcome to EasyGen - Verify Your Email",
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"  # Main content is now text/html
            email.send()

            return Response({
                'message': "Verification email sent. Please verify your account.",
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'phone_number': user.phone_number,
                    'zip_code': user.zip_code
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid credentials',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.user
        
        if not user.is_verified:
            return Response({
                'status': 'error',
                'message': 'Your account is not verified. Please verify your email first.'
            }, status=status.HTTP_403_FORBIDDEN)

        response = super().post(request, *args, **kwargs)
        
        # Add user data to response
        response.data.update({
            'status': 'success',
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'zip_code': user.zip_code
            }
        })
        
        return response


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        from backend.models import CustomUser

        try:
            # Decode the uidb64 parameter
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
            except (TypeError, ValueError, UnicodeDecodeError):
                return render(request, 'email_verification_success.html', {
                    'error': 'Invalid verification link. Please request a new verification email.'
                })

            # Get the user
            try:
                user = get_object_or_404(CustomUser, pk=uid)
            except CustomUser.DoesNotExist:
                return render(request, 'email_verification_success.html', {
                    'error': 'User not found. Please request a new verification email.'
                })

            # Check if user is already verified
            if user.is_verified:
                return render(request, 'email_verification_already_verified.html')

            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return render(request, 'email_verification_success.html', {
                    'success': True,
                    'message': 'Your email has been verified successfully!'
                })
            else:
                return render(request, 'email_verification_expired.html')
        except Exception as e:
            return render(request, 'email_verification_success.html', {
                'error': 'An error occurred during verification. Please try again.'
            })


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'status': 'success',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'zip_code': user.zip_code,
                'is_verified': user.is_verified
            }
        }, status=status.HTTP_200_OK)