import json
import time
from tqdm import tqdm
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File paths
file_path = './linkedin_templates.json'
output_file_path = './template_embeddings.json'

# Load templates
with open(file_path, "r", encoding="utf-8") as f:
    templates = json.load(f)

# Embedding function using new SDK
def get_embedding(text, model="text-embedding-ada-002"):
    for _ in range(3):
        try:
            response = client.embeddings.create(input=text, model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error: {e}. Retrying in 1 second...")
            time.sleep(1)
    raise Exception(f"Failed to get embedding for: {text}")

# Generate and store embeddings
embedded_templates = []
for template in tqdm(templates, desc="Embedding purposes"):
    embedding = get_embedding(template["purpose"])
    embedded_templates.append({
        "id": template["id"],
        "template_name": template["template_name"],
        "purpose": template["purpose"],
        "fields": template["fields"],
        "template_text": template["template_text"],
        "embedding": embedding
    })

# Save to output file
with open(output_file_path, "w", encoding="utf-8") as out:
    json.dump(embedded_templates, out, indent=2)

print(f"✅ Embeddings saved to {output_file_path}")
