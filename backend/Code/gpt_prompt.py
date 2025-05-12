def system_prompt(k):
    return f"""
You are a professional LinkedIn post generator.

You will receive:
- A topic the user wants to post about
- {k} LinkedIn post templates (each with a purpose and structural format)
- The user's preferences (industry, role, tone, writing style, goals, etc.)

Your task:
- Generate {k} original LinkedIn posts, one for each structure provided
- Use the structure to shape the post naturally (modifications are allowed if needed)
- Ensure each post aligns with the user's preferences in tone and style
- Make it sound authentic and human — not robotic or templated

Formatting rules:
- Do NOT mention template names or structure metadata
- Do NOT include variables like {{x}}, {{tip_1}}, etc.
- Use clean, short paragraphs formatted for LinkedIn
- Add a soft CTA if it fits the flow
- Use emojis only if they add meaning (1–2 max)
"""


def generate_prompt(topic, templates, prefs, k):
    prompt = f"""The user wants to generate LinkedIn posts about the topic: "{topic}"

Here are their content preferences:
- Content types: {", ".join(prefs['content_types'])}
- Posting goals: {", ".join(prefs['posting_goals'])}
- Industries: {", ".join(prefs['industries'])}
- Roles: {", ".join(prefs['job_descriptions'])}
- Writing style: {", ".join(prefs['writing_styles'])}
- Tone adjustment: {prefs['fine_tune_description']}
- CTA adjustment: {prefs['modify_post_cta']}

Below are {k} LinkedIn post structures you should use to write the posts.
Use them only as guidance — modify where necessary to fit the topic and sound natural.
"""

    for i, template in enumerate(templates, start=1):
        prompt += f"\n---\nStructure {i}:\n{template['template_text']}\n"

    prompt += f"""

Your task is to generate {k} distinct LinkedIn posts, each based on one structure.

Important:
- Do NOT include placeholder variables like {{x}}, {{tip_1}}, etc.
- Do NOT reference templates or structure numbers
- Write each post as if it's ready to publish
- Make sure the writing feels human, helpful, and well-formatted for LinkedIn
"""
    return prompt
