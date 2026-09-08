import re
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/140.0 Mobile Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def search(username):
    username = username.strip().lstrip("@")
    url = f"https://www.tiktok.com/@{username}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            allow_redirects=True
        )
    except requests.RequestException:
        return None

    if response.status_code == 404:
        return None

    if response.status_code in (401, 403, 429):
        return {
            "username": username,
            "profile_url": url,
            "status": "RESTRICTED",
            "http_status": response.status_code
        }

    if response.status_code != 200:
        return {
            "username": username,
            "profile_url": url,
            "status": f"HTTP {response.status_code}"
        }

    html = response.text

    result = {
        "username": username,
        "profile_url": response.url,
        "status": "FOUND"
    }

    title = re.search(
        r"<title>(.*?)</title>",
        html,
        re.I | re.S
    )

    if title:
        result["page_title"] = title.group(1).strip()

    description = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if description:
        result["description"] = description.group(1)

    image = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if image:
        result["profile_image"] = image.group(1)

    og_description = re.search(
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S
    )

    if og_description:
        result["bio"] = og_description.group(1)

    scripts = re.findall(
        r'<script[^>]*id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S
    )

    for script in scripts:
        try:
            data = json.loads(script)

            result["public_metadata"] = data

        except (json.JSONDecodeError, TypeError):
            continue

    return result
