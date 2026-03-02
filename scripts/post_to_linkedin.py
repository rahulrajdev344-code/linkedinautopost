"""
Post content to LinkedIn using the LinkedIn v2 API.
"""

import os
import json
import requests

LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.environ.get("LINKEDIN_PERSON_URN", "")
LINKEDIN_API_URL = "https://api.linkedin.com/v2/ugcPosts"


def post_to_linkedin(content: str) -> dict:
    """
    Publish a text post to LinkedIn on the authenticated user's profile.

    Args:
        content: The text content to post.

    Returns:
        dict with 'success' (bool) and 'details' (str or dict).
    """
    if not LINKEDIN_ACCESS_TOKEN:
        raise ValueError("LINKEDIN_ACCESS_TOKEN environment variable is not set")
    if not LINKEDIN_PERSON_URN:
        raise ValueError("LINKEDIN_PERSON_URN environment variable is not set")

    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    payload = {
        "author": f"urn:li:person:{LINKEDIN_PERSON_URN}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }

    response = requests.post(LINKEDIN_API_URL, headers=headers, json=payload)

    if response.status_code in (200, 201):
        result = response.json()
        post_id = result.get("id", "unknown")
        return {
            "success": True,
            "details": f"Post published successfully! Post ID: {post_id}",
        }
    else:
        return {
            "success": False,
            "details": {
                "status_code": response.status_code,
                "error": response.text,
            },
        }


if __name__ == "__main__":
    # Test with a sample post
    test_content = "This is a test post from the LinkedIn Auto Poster! 🚀"
    result = post_to_linkedin(test_content)
    print(json.dumps(result, indent=2))

