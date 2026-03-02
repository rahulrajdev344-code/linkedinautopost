"""
One-time helper script to get your LinkedIn Person URN.

Usage:
    Set LINKEDIN_ACCESS_TOKEN env variable or paste it when prompted.
    python get_person_urn.py
"""

import os
import sys
import requests


def get_person_urn(access_token: str) -> str:
    """Fetch the authenticated user's LinkedIn person URN."""
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    # Use the userinfo endpoint to get the sub (person ID)
    response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)

    if response.status_code == 200:
        data = response.json()
        person_id = data.get("sub", "")
        name = data.get("name", "Unknown")
        email = data.get("email", "Unknown")
        return person_id, name, email
    else:
        print(f"ERROR: API returned status {response.status_code}")
        print(response.text)
        sys.exit(1)


def main():
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")

    if not access_token:
        access_token = input("Paste your LinkedIn Access Token: ").strip()

    if not access_token:
        print("ERROR: No access token provided.")
        sys.exit(1)

    person_id, name, email = get_person_urn(access_token)

    print()
    print("=" * 60)
    print("LinkedIn Profile Info")
    print("=" * 60)
    print(f"  Name:       {name}")
    print(f"  Email:      {email}")
    print(f"  Person ID:  {person_id}")
    print()
    print("NEXT STEPS:")
    print(f"1. Go to your GitHub repo → Settings → Secrets → Actions")
    print(f"2. Add secret: LINKEDIN_PERSON_URN = {person_id}")
    print()


if __name__ == "__main__":
    main()
