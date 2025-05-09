from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ContentTypeViewSet, PostingGoalViewSet, WritingStyleViewSet, IndustryViewSet,
    JobDescriptionViewSet, UserPreferenceViewSet, UserPreferenceSelectionViewSet,
    PackageViewSet, SubscriptionViewSet
)
from .ViralPostGeneration import GenerateLinkedInPostFromTitleAPIView


router = DefaultRouter()
router.register(r'api/content-types', ContentTypeViewSet, basename='contenttype')
router.register(r'api/posting-goals', PostingGoalViewSet, basename='postinggoal')
router.register(r'api/writing-styles', WritingStyleViewSet, basename='writingstyle')
router.register(r'api/industries', IndustryViewSet, basename='industry')
router.register(r'api/job-descriptions', JobDescriptionViewSet, basename='jobdescription')
router.register(r'api/packages', PackageViewSet, basename='package')
router.register(r'api/subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('api/user-preferences/', UserPreferenceViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update'
    }), name='user-preference'),

    path('api/user-preference-selections/', UserPreferenceSelectionViewSet.as_view({
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'get': 'retrieve'
    }), name='user-preference-selections'),

    path('api/user-preference-selections/mine/', UserPreferenceSelectionViewSet.as_view({
        'get': 'mine'
    }), name='user-preference-selections-mine'),



    path('api/generate-linkedin-post/', GenerateLinkedInPostFromTitleAPIView.as_view(), name='generate-linkedin-post'),


]

urlpatterns += router.urls
