"""
One-time helper script to get a LinkedIn OAuth2 access token.

Prerequisites:
1. Create a LinkedIn Developer App at https://www.linkedin.com/developers/apps
2. Enable "Share on LinkedIn" and "Sign In with LinkedIn using OpenID Connect" products
3. Set redirect URL to: http://localhost:8080/callback
4. Note your Client ID and Client Secret from the Auth tab

Usage:
    python get_linkedin_token.py
"""

import http.server
import urllib.parse
import webbrowser
import requests
import json
import sys

# ============================================================
# FILL THESE IN with your LinkedIn app credentials
# ============================================================
CLIENT_ID = ""      # <-- Paste your Client ID here
CLIENT_SECRET = ""  # <-- Paste your Client Secret here
# ============================================================

REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "openid profile w_member_social"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

authorization_code = None


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handle the OAuth callback from LinkedIn."""

    def do_GET(self):
        global authorization_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            authorization_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization successful!</h1>"
                b"<p>You can close this window and return to the terminal.</p>"
                b"</body></html>"
            )
        else:
            error = params.get("error", ["unknown"])[0]
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>Error: {error}</h1></body></html>".encode()
            )

    def log_message(self, format, *args):
        pass  # Suppress server logs


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: Please fill in CLIENT_ID and CLIENT_SECRET in this file first!")
        print("Get them from: https://www.linkedin.com/developers/apps → Your App → Auth tab")
        sys.exit(1)

    # Step 1: Open browser for user authorization
    auth_params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": "linkedin_auto_poster",
    })
    auth_full_url = f"{AUTH_URL}?{auth_params}"

    print("=" * 60)
    print("LinkedIn OAuth2 Token Generator")
    print("=" * 60)
    print()
    print("Opening your browser for LinkedIn authorization...")
    print("If the browser doesn't open, visit this URL manually:")
    print()
    print(auth_full_url)
    print()

    webbrowser.open(auth_full_url)

    # Step 2: Start local server to receive the callback
    print("Waiting for authorization callback on http://localhost:8080 ...")
    server = http.server.HTTPServer(("localhost", 8080), OAuthCallbackHandler)
    server.handle_request()  # Handle one request then stop

    if not authorization_code:
        print("ERROR: No authorization code received.")
        sys.exit(1)

    print("Authorization code received! Exchanging for access token...")

    # Step 3: Exchange auth code for access token
    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=token_data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info["access_token"]
        expires_in = token_info.get("expires_in", "unknown")

        print()
        print("=" * 60)
        print("SUCCESS! Here is your access token:")
        print("=" * 60)
        print()
        print(access_token)
        print()
        print(f"Expires in: {expires_in} seconds (~{int(expires_in)//86400} days)")
        print()
        print("NEXT STEPS:")
        print("1. Copy the access token above")
        print("2. Go to your GitHub repo → Settings → Secrets → Actions")
        print("3. Add secret: LINKEDIN_ACCESS_TOKEN = <paste token>")
        print()
        print("⚠️  This token expires in ~60 days. You'll need to re-run this script to get a new one.")
    else:
        print(f"ERROR: Failed to get access token. Status: {response.status_code}")
        print(response.text)
        sys.exit(1)


if __name__ == "__main__":
    main()
