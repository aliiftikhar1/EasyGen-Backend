# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.shortcuts import get_object_or_404

# --- Simple GET-only ViewSets for each option ---
class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name'))
        return Response(data)

class PostingGoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostingGoal.objects.all()
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name'))
        return Response(data)

class WritingStyleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WritingStyle.objects.all()
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name'))
        return Response(data)

class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name'))
        return Response(data)

class JobDescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobDescription.objects.all()
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name'))
        return Response(data)

class UserPreferenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_or_create_preference(self, user):
        pref, _ = UserPreference.objects.get_or_create(user=user)
        return pref

    def retrieve(self, request):
        pref = self.get_or_create_preference(request.user)
        return Response({
            'id': pref.id,
            'fine_tune_description': pref.fine_tune_description,
            'modify_post_cta': pref.modify_post_cta
        })

    def update(self, request):
        pref = self.get_or_create_preference(request.user)
        pref.fine_tune_description = request.data.get('fine_tune_description', pref.fine_tune_description)
        pref.modify_post_cta = request.data.get('modify_post_cta', pref.modify_post_cta)
        pref.save()
        return Response({
            'id': pref.id,
            'fine_tune_description': pref.fine_tune_description,
            'modify_post_cta': pref.modify_post_cta
        })

    def partial_update(self, request):
        return self.update(request)
    
# --- User Preference Selection ---
class UserPreferenceSelectionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_pref_selection(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        selection, _ = UserPreferenceSelection.objects.get_or_create(user_preference=pref)
        return selection

    def retrieve(self, request):
        selection = self.get_pref_selection(request)
        return Response(self._serialize_selection(selection))

    def mine(self, request):
        selection = self.get_pref_selection(request)
        return Response(self._serialize_selection(selection))

    def create(self, request):
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        if UserPreferenceSelection.objects.filter(user_preference=pref).exists():
            return Response({'detail': 'Already exists. Use PUT/PATCH.'}, status=400)
        
        selection = UserPreferenceSelection.objects.create(user_preference=pref)
        self._update_selection(selection, request.data)
        return Response(self._serialize_selection(selection), status=201)

    def update(self, request):
        selection = self.get_pref_selection(request)
        self._update_selection(selection, request.data)
        return Response(self._serialize_selection(selection))
    
    def partial_update(self, request):
        return self.update(request)

    def _serialize_selection(self, selection):
        return {
            'id': selection.id,
            'content_types': list(selection.content_types.values('id', 'name')),
            'posting_goals': list(selection.posting_goals.values('id', 'name')),
            'writing_styles': list(selection.writing_styles.values('id', 'name')),
            'industries': list(selection.industries.values('id', 'name')),
            'job_descriptions': list(selection.job_descriptions.values('id', 'name')),
            'user_preference': {
                'id': selection.user_preference.id,
                'fine_tune_description': selection.user_preference.fine_tune_description,
                'modify_post_cta': selection.user_preference.modify_post_cta
            }
        }

    def _update_selection(self, selection, data):
        if 'content_types' in data:
            selection.content_types.set(data['content_types'])
        if 'posting_goals' in data:
            selection.posting_goals.set(data['posting_goals'])
        if 'writing_styles' in data:
            selection.writing_styles.set(data['writing_styles'])
        if 'industries' in data:
            selection.industries.set(data['industries'])
        if 'job_descriptions' in data:
            selection.job_descriptions.set(data['job_descriptions'])
        selection.save()

# --- Packages ---
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.filter(is_active=True)
    
    def list(self, request):
        data = list(self.queryset.values('id', 'name', 'description', 'monthly_price', 'yearly_price'))
        return Response(data)

class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def list(self, request):
        subscriptions = self.get_queryset()
        data = []
        for sub in subscriptions:
            data.append({
                'id': sub.id,
                'package': sub.package.id,
                'billing_cycle': sub.billing_cycle,
                'start_date': sub.start_date,
                'end_date': sub.end_date,
                'is_active': sub.is_active
            })
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)