from django.contrib import admin
from .models import *




admin.site.register(CustomUser)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'fine_tune_description', 'modify_post_cta')
    search_fields = ('user__username',)

@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PostingGoal)
class PostingGoalAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(WritingStyle)
class WritingStyleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserPreferenceSelection)
class UserPreferenceSelectionAdmin(admin.ModelAdmin):
    list_display = ('user_preference',)
    filter_horizontal = ('content_types', 'posting_goals', 'writing_styles', 'industries', 'job_descriptions')
    search_fields = ('user_preference__user__username',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user',)