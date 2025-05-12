import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from backend.Code.utils import load_user_preferences
from backend.Code.generate_post import generate_post
from .models import UserPreference, UserPreferenceSelection


import re
from textwrap import wrap


def format_linkedin_post(text):
    if not text:
        return ""

    # Remove markdown and structure phrases
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold markdown
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove italics
    text = re.sub(r'(?i)\d\.\s*(hook|story|insight|takeaway|cta|call to action):?', '', text)  # Remove headings
    text = re.sub(r'(?i)(hook|story|takeaway|cta|call to action):', '', text)  # Remove non-numbered ones too
    text = re.sub(r'(?i)okay.*?here(\'s| is)', '', text, count=1)  # Remove “okay here’s a...” intros
    text = re.sub(r'^[\W_]+', '', text.strip())  # Clean up any leftover punctuation at start

    # Normalize spacing
    text = text.replace('\r\n', '\n').replace('\r', '\n').strip()
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    text = "\n\n".join(paragraphs)

    wrapped_lines = []
    for paragraph in text.split("\n\n"):
        wrapped = "\n".join(wrap(paragraph, width=100))
        wrapped_lines.append(wrapped)

    return "\n\n".join(wrapped_lines)



class GenerateLinkedInPostFromTitleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        user = request.user

        user_preferences = load_user_preferences(request)


        if not title:
            return Response({'error': 'Title is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(f"Generating posts...")
            response = generate_post(title, user_preferences, num_of_posts=1)
            # formatted_post = format_linkedin_post(response)
            formatted_post = "Check command prompt"
            return Response(response["post_1"])
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
