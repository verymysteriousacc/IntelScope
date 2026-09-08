import re
import requests

HEADERS = {
    "User-Agent": "IntelScope/1.0 (Public OSINT Research)"
}

def search(username):
    username = username.strip().lstrip("@")

    if not username.isdigit():
        return {
            "username": username,
            "status": "LIMITED",
            "reason": "Discord does not provide unauthenticated username-to-profile lookup.",
            "supported_input": "Public Discord user ID",
            "note": "No authentication or restriction bypass is attempted."
        }

    user_id = username
    url = f"https://discord.com/users/{user_id}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )
    except requests.RequestException:
        return None

    return {
        "user_id": user_id,
        "profile_url": url,
        "status": (
            "FOUND"
            if response.status_code == 200
            else f"HTTP {response.status_code}"
        )
  }
