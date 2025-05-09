from rest_framework import serializers
from .models import (
    ContentType, PostingGoal, WritingStyle, Industry, JobDescription,
    UserPreference, UserPreferenceSelection, Package, Subscription
)

# --- Basic Option Serializers ---
class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'

class PostingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostingGoal
        fields = '__all__'

class WritingStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingStyle
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'

# --- Simple Name Serializer for nested use ---
class NameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType  # reused for all
        fields = ['id', 'name']

# --- User Preference ---
class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['id', 'fine_tune_description', 'modify_post_cta']

# --- Full Selection Serializer for GET ---
class UserPreferenceSelectionSerializer(serializers.ModelSerializer):
    content_types = NameOnlySerializer(many=True, read_only=True)
    posting_goals = NameOnlySerializer(many=True, read_only=True)
    writing_styles = NameOnlySerializer(many=True, read_only=True)
    industries = NameOnlySerializer(many=True, read_only=True)
    job_descriptions = NameOnlySerializer(many=True, read_only=True)
    user_preference = UserPreferenceSerializer(read_only=True)

    class Meta:
        model = UserPreferenceSelection
        fields = '__all__'

# --- For create/update ---
class UserPreferenceSelectionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferenceSelection
        fields = ['content_types', 'posting_goals', 'writing_styles', 'industries', 'job_descriptions']

# --- Other Models ---
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
