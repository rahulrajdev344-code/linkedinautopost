"""
Generate a tech-related LinkedIn post using OpenRouter API (DeepSeek R1 free model).
"""

import os
import json
import random
from pathlib import Path
from openai import OpenAI

# OpenRouter config
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-r1"

# Path to topics file
TOPICS_FILE = Path(__file__).parent.parent / "config" / "topics.json"

SYSTEM_PROMPT = """You are a senior tech professional and thought leader who writes engaging LinkedIn posts. 
Your posts are insightful, practical, and spark conversations.

Rules for writing the post:
1. Start with a strong hook (first line should grab attention — use a bold statement, question, or surprising fact)
2. Keep it between 150-250 words
3. Use short paragraphs (1-3 sentences each) for mobile readability
4. Include practical insights or actionable tips, not just generic fluff
5. End with a question or call-to-action to drive engagement
6. Add 3-5 relevant hashtags at the end
7. Use a conversational yet professional tone
8. Include line breaks between paragraphs for readability
9. Do NOT use markdown formatting (no **, no ##, no bullet points with *)
10. Use emojis sparingly (1-3 max) to add personality
11. Do NOT start with "I" — start with the hook
12. Make it feel authentic and human, not AI-generated
13. Do NOT include any thinking tags, reasoning, or meta-commentary — output ONLY the LinkedIn post text"""


def load_random_topic() -> str:
    """Load a random tech topic from the topics config file."""
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return random.choice(data["topics"])


def generate_post(topic: str | None = None) -> str:
    """Generate a LinkedIn post about the given topic using OpenRouter."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")

    if topic is None:
        topic = load_random_topic()

    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

    user_prompt = f"""Write a LinkedIn post about: {topic}

Make it fresh, insightful, and unique. Share a perspective that most people haven't considered.
Include a real-world example or analogy to make the concept relatable."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0.9,
        extra_headers={
            "HTTP-Referer": "https://github.com/linkedin-auto-poster",
            "X-Title": "LinkedIn Auto Poster",
        },
    )

    post_content = response.choices[0].message.content.strip()

    # Clean up any thinking tags that DeepSeek R1 might include
    if "<think>" in post_content:
        # Remove everything between <think> and </think> tags
        import re
        post_content = re.sub(r"<think>.*?</think>", "", post_content, flags=re.DOTALL).strip()

    return post_content


if __name__ == "__main__":
    topic = load_random_topic()
    print(f"Topic: {topic}\n")
    print("=" * 50)
    post = generate_post(topic)
    print(post)
