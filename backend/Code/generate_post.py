# generates_posts.py

import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from django.conf import settings
from backend.Code.utils import load_user_preferences, get_random_linkedin_profile
from backend.Code.gpt_prompt import generate_prompt, system_prompt


load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)



def generate_post(topic, preferences):
    # Ensure list-like formatting for preferences
    def str_to_list(value):
        return [item.strip() for item in value.split(',')] if isinstance(value, str) else value

    preferences = {
        "content_types": str_to_list(preferences.get("content_types", [])),
        "posting_goals": str_to_list(preferences.get("posting_goals", [])),
        "industries": str_to_list(preferences.get("industries", [])),
        "job_descriptions": str_to_list(preferences.get("job_descriptions", [])),
        "writing_styles": str_to_list(preferences.get("writing_styles", [])),
        "fine_tune_description": preferences.get("fine_tune_description", ""),
        "modify_post_cta": preferences.get("modify_post_cta", "")
    }

    profile = get_random_linkedin_profile()
    print(f"Using profile: {profile}")
    
    s_prompt = system_prompt(profile)
    prompt = generate_prompt(topic, preferences)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": s_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Failed to generate post: {e}")
        return f"Error: {e}"
