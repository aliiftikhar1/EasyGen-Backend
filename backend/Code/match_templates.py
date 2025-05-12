import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEMPLATE_EMBEDDINGS_FILE = './backend/Code/template_embeddings.json'

# Load template embeddings
with open(TEMPLATE_EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
    template_data = json.load(f)

# Function to get embedding for user input
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

# Cosine similarity
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Match user topic to templates
import time

def find_best_templates(user_topic, top_k=1):
    start_time = time.time()

    user_embedding = get_embedding(user_topic)
    scored_templates = []

    for template in template_data:
        similarity = cosine_similarity(user_embedding, template["embedding"])
        template_copy = {k: v for k, v in template.items() if k != "embedding"}
        scored_templates.append((similarity, template_copy))

    # Sort by descending similarity
    scored_templates.sort(reverse=True, key=lambda x: x[0])

    # Track time
    elapsed = round(time.time() - start_time, 4)
    print(f"[INFO] - Time for getting top {top_k} matched templates for topic '{user_topic}': {elapsed}s")

    # Return only the template dicts (without embeddings)
    return [tpl for _, tpl in scored_templates[:top_k]]


# Example usage
if __name__ == "__main__":
    topic = input("Enter a topic (e.g., 'I love cookies'): ").strip()
    top_templates = find_best_templates(topic)

    print(f"\nTop templates for: '{topic}'\n")
    for score, template in top_templates:
        print(f"→ {template['template_name']} (score: {score:.4f})")
        print(f"Purpose: {template['purpose']}")
        print('-' * 60)
