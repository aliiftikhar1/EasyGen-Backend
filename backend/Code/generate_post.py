# generate_post.py

import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from django.conf import settings
from backend.Code.gpt_prompt import generate_prompt, system_prompt
from backend.Code.match_templates import find_best_templates

load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# Modified generate_post function to properly handle the JSON response

# Modified generate_post function with robust JSON handling

def generate_post(topic, preferences, num_of_posts=5):
    import time
    import json
    import re

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

    start = time.time()
    templates = find_best_templates(topic, top_k=num_of_posts)
    duration = time.time() - start
    print(f"[INFO] - Time for getting top {num_of_posts} matched templates for topic '{topic}': {duration:.4f}s")

    s_prompt = system_prompt(num_of_posts)
    user_prompt = generate_prompt(topic, templates, preferences, num_of_posts)

    # Use a different approach - ask for each post individually
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": s_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=3000,  # Increase token limit
    )

    # Get the full text response
    full_response = response.choices[0].message.content
    
    # Extract posts using regex pattern matching
    posts = {}
    
    # Try to extract posts based on common patterns in the response
    try:
        # Method 1: Look for post numbering patterns
        post_pattern = re.compile(r'(Post|POST|LinkedIn Post|#) (\d+)[:\s-]*\n(.*?)(?=(?:Post|POST|LinkedIn Post|#) \d+[:\s-]*\n|$)', re.DOTALL)
        matches = post_pattern.findall(full_response)
        
        if matches:
            for _, num, content in matches:
                posts[f"post_{num}"] = content.strip()
        
        # If regex didn't find posts, try splitting by common separators
        if not posts:
            sections = re.split(r'---+|\*\*\*+|={3,}', full_response)
            if len(sections) >= num_of_posts:
                for i, section in enumerate(sections[:num_of_posts], 1):
                    posts[f"post_{i}"] = section.strip()
        
        # If still no posts found, split the content evenly
        if not posts:
            paragraphs = [p for p in full_response.split('\n\n') if p.strip()]
            posts_per_section = max(1, len(paragraphs) // num_of_posts)
            
            for i in range(num_of_posts):
                start_idx = i * posts_per_section
                end_idx = start_idx + posts_per_section if i < num_of_posts - 1 else len(paragraphs)
                if start_idx < len(paragraphs):
                    content = '\n\n'.join(paragraphs[start_idx:end_idx])
                    posts[f"post_{i+1}"] = content.strip()
    
    except Exception as e:
        print(f"Error processing posts: {e}")
        # Fallback: Just return the full response
        posts = {"post_1": full_response}
    
    # Fill in any missing posts with placeholders
    for i in range(1, num_of_posts + 1):
        key = f"post_{i}"
        if key not in posts:
            posts[key] = f"Error generating post {i}."
    
    return posts