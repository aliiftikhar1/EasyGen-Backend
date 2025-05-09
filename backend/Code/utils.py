import json
import random
from backend.models import UserPreference, UserPreferenceSelection
import os

def load_user_preferences(request):
    user = request.user

    try:
        user_pref = UserPreference.objects.get(user=user)
        selection = UserPreferenceSelection.objects.get(user_preference=user_pref)
    except UserPreference.DoesNotExist:
        print("User preferences not found.")
        return {}
    except UserPreferenceSelection.DoesNotExist:
        print("User preference selections not found.")
        return {}

    def list_names(qs):
        return ", ".join([item.name for item in qs.all()]) if qs.exists() else "N/A"

    return {
        "content_types": list_names(selection.content_types),
        "posting_goals": list_names(selection.posting_goals),
        "writing_styles": list_names(selection.writing_styles),
        "industries": list_names(selection.industries),
        "job_descriptions": list_names(selection.job_descriptions),
        "fine_tune_description": user_pref.fine_tune_description or "",
        "modify_post_cta": user_pref.modify_post_cta or ""
    }


def get_random_linkedin_profile(file_path='backend/Code/linkedin_profiles.txt'):
    try:
        # Use os.path for safe cross-platform path handling
        abs_path = os.path.abspath(file_path)
        with open(abs_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
        if not lines:
            raise ValueError("The file is empty.")
        return random.choice(lines)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
